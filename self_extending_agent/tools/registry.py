"""
Tool registry for storing and retrieving tools.
"""
import json
import os
import importlib.util
import inspect
from typing import Dict, List, Any, Optional, Callable
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
REGISTRY_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(REGISTRY_DIR, "generated")
METADATA_FILE = os.path.join(REGISTRY_DIR, "tool_registry.json")

# Ensure directories exist
os.makedirs(GENERATED_DIR, exist_ok=True)

class ToolRegistry:
    """Registry for storing and retrieving tools."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Load tool metadata from JSON file."""
        if os.path.exists(METADATA_FILE):
            try:
                with open(METADATA_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Error decoding {METADATA_FILE}, creating new registry")
                return {}
        return {}
    
    def _save_metadata(self):
        """Save tool metadata to JSON file."""
        with open(METADATA_FILE, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def register_tool(self, name: str, description: str, params: Dict[str, Dict[str, Any]], 
                      code: str, examples: List[Dict[str, Any]] = None) -> bool:
        """
        Register a new tool in the registry.
        
        Args:
            name: Tool name (should be valid Python identifier)
            description: Tool description
            params: Parameter schema (name, type, description)
            code: Python code for the tool
            examples: Example usages with inputs and expected outputs
            
        Returns:
            bool: Success or failure
        """
        # Sanitize name for filename
        module_name = name.replace('-', '_').replace(' ', '_').lower()
        file_path = os.path.join(GENERATED_DIR, f"{module_name}.py")
        
        # Check if tool already exists
        if name in self.metadata:
            logger.warning(f"Tool {name} already exists")
            return False
        
        # Write code to file
        try:
            with open(file_path, 'w') as f:
                f.write(code)
            
            # Add metadata
            self.metadata[name] = {
                "description": description,
                "params": params,
                "module_name": module_name,
                "file_path": file_path,
                "examples": examples or []
            }
            self._save_metadata()
            logger.info(f"Registered tool: {name}")
            return True
        
        except Exception as e:
            logger.error(f"Error registering tool {name}: {str(e)}")
            # Clean up if file was created
            if os.path.exists(file_path):
                os.remove(file_path)
            return False
    
    def get_tool_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific tool."""
        return self.metadata.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools with their metadata."""
        return [
            {
                "name": name,
                "description": meta["description"],
                "params": meta["params"],
                "examples": meta.get("examples", [])
            }
            for name, meta in self.metadata.items()
        ]
    
    def load_tool(self, name: str) -> Optional[Callable]:
        """
        Load a tool's implementation.
        
        Args:
            name: Tool name
            
        Returns:
            Callable: The tool function if found, None otherwise
        """
        if name not in self.metadata:
            logger.warning(f"Tool {name} not found")
            return None
        
        meta = self.metadata[name]
        file_path = meta["file_path"]
        module_name = meta["module_name"]
        
        try:
            # Load module dynamically
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                logger.error(f"Could not load spec for {module_name}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find the function in the module
            # We expect the function to have the same name as the module
            for item_name, item in inspect.getmembers(module, inspect.isfunction):
                # Return the first function defined in the module
                return item
            
            logger.error(f"No function found in module {module_name}")
            return None
            
        except Exception as e:
            logger.error(f"Error loading tool {name}: {str(e)}")
            return None

# Global instance
registry = ToolRegistry()
