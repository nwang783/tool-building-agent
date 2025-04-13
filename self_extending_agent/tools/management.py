"""
Tool management functions for agents to create, get, and use tools.
"""
import inspect
import json
from typing import Any, Dict, List, Optional, Union

from agents import FunctionTool, function_tool, RunContextWrapper
from pydantic import BaseModel, create_model

from .registry import registry

# Models for tool creation
class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True

class ToolExample(BaseModel):
    inputs: Dict[str, Any]
    output: Any

class ToolCreationParams(BaseModel):
    name: str
    description: str
    parameters: List[ToolParameter]
    code: str
    examples: Optional[List[ToolExample]] = None

# Function to create pydantic model schema from parameters
def _create_schema_from_params(params: List[ToolParameter]) -> Dict[str, Any]:
    """Create a JSON schema from parameter definitions."""
    properties = {}
    required = []
    
    for param in params:
        # Convert string type to Python type
        type_map = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        param_type = type_map.get(param.type.lower(), str)
        
        # Add to properties
        properties[param.name] = (
            param_type, 
            {"description": param.description}
        )
        
        if param.required:
            required.append(param.name)
    
    # Create dynamic model
    model = create_model("ToolParams", **properties)
    
    # Extract JSON schema
    schema = model.model_json_schema()
    if required:
        schema["required"] = required
    
    return schema

@function_tool
def get_tools() -> str:
    """
    Get a list of all available tools with their metadata and usage examples.
    
    Returns:
        str: JSON string with tool information
    """
    tools = registry.list_tools()
    return json.dumps(tools, indent=2)

@function_tool
def use_tool(tool_name: str, params: str) -> str:
    """
    Execute a tool with the given parameters.
    
    Args:
        tool_name: Name of the tool to use
        params: JSON string of parameters to pass to the tool
        
    Returns:
        str: Result of the tool execution
    """
    # Load the tool
    tool_func = registry.load_tool(tool_name)
    if not tool_func:
        return json.dumps({"error": f"Tool {tool_name} not found"})
    
    # Parse params
    try:
        params_dict = json.loads(params)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format for parameters"})
    
    # Execute the tool
    try:
        result = tool_func(**params_dict)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": f"Error executing tool: {str(e)}"})

@function_tool
def create_tool(specification: str) -> str:
    """
    Create a new tool based on specifications.
    
    Args:
        specification: JSON string with tool specifications including name, 
                      description, parameters, and implementation code
                      
    Returns:
        str: Result of tool creation process
    """
    try:
        # Parse specification
        spec_dict = json.loads(specification)
        spec = ToolCreationParams(**spec_dict)
        
        # Register the tool
        success = registry.register_tool(
            name=spec.name,
            description=spec.description,
            params={p.name: {"type": p.type, "description": p.description, "required": p.required} 
                   for p in spec.parameters},
            code=spec.code,
            examples=[e.dict() for e in spec.examples] if spec.examples else None
        )
        
        if success:
            return json.dumps({
                "status": "success",
                "message": f"Tool {spec.name} created successfully"
            })
        else:
            return json.dumps({
                "status": "error",
                "message": f"Failed to create tool {spec.name}"
            })
            
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error creating tool: {str(e)}"
        })

# Export the function tools for use with agents
get_tools_tool = get_tools
use_tool_tool = use_tool
create_tool_tool = create_tool
