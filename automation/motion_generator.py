#!/usr/bin/env python3
"""
Legal Motion Generator for Hawaii Family Court
Automated document creation with LaTeX compilation
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class HawaiiMotionGenerator:
    """Generates legal motions for Hawaii Family Court proceedings"""
    
    def __init__(self, case_number="1FDV-23-0001009"):
        self.case_number = case_number
        self.templates_dir = Path("templates")
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def load_template(self, template_name: str) -> str:
        """Load LaTeX template from templates directory"""
        template_path = self.templates_dir / f"{template_name}.tex"
        if not template_path.exists():
            raise FileNotFoundError(f"Template {template_name} not found")
        return template_path.read_text()
        
    def generate_motion(self, motion_type: str, parameters: Dict[str, Any]) -> str:
        """Generate motion document from template and parameters"""
        template = self.load_template("hawaii_motion_template")
        
        # Replace placeholders with actual content
        replacements = {
            "[MOTION_TITLE]": parameters.get("title", "UNTITLED MOTION"),
            "[INTRODUCTION_CONTENT]": parameters.get("introduction", ""),
            "[BACKGROUND_CONTENT]": parameters.get("background", ""),
            "[LEGAL_STANDARD_CONTENT]": parameters.get("legal_standard", ""),
            "[ARGUMENT_CONTENT]": parameters.get("argument", ""),
            "[CONCLUSION_CONTENT]": parameters.get("conclusion", ""),
            "[RELIEF_REQUESTED]": parameters.get("relief", ""),
            "[DATE]": datetime.now().strftime("%B %d, %Y"),
            "[ADDRESS]": parameters.get("address", "[ADDRESS TO BE PROVIDED]"),
            "[PHONE]": parameters.get("phone", "[PHONE TO BE PROVIDED]"),
            "[EMAIL]": parameters.get("email", "[EMAIL TO BE PROVIDED]")
        }
        
        document = template
        for placeholder, replacement in replacements.items():
            document = document.replace(placeholder, replacement)
            
        return document
        
    def save_motion(self, motion_content: str, filename: str) -> Path:
        """Save motion to output directory"""
        output_path = self.output_dir / filename
        output_path.write_text(motion_content)
        return output_path
        
    def compile_latex(self, tex_file: Path) -> Path:
        """Compile LaTeX file to PDF"""
        import subprocess
        
        try:
            subprocess.run(["pdflatex", "-output-directory", str(self.output_dir), str(tex_file)], 
                         check=True, capture_output=True)
            pdf_path = self.output_dir / f"{tex_file.stem}.pdf"
            return pdf_path
        except subprocess.CalledProcessError as e:
            print(f"LaTeX compilation failed: {e.stderr.decode()}")
            raise
            
def main():
    parser = argparse.ArgumentParser(description="Generate legal motions for Hawaii Family Court")
    parser.add_argument("--type", required=True, choices=["compel", "sanctions", "modify", "emergency"],
                       help="Type of motion to generate")
    parser.add_argument("--config", default="config/motion_config.json",
                       help="Configuration file with motion parameters")
    parser.add_argument("--compile", action="store_true",
                       help="Compile LaTeX to PDF")
    
    args = parser.parse_args()
    
    # Load configuration
    with open(args.config) as f:
        config = json.load(f)
    
    # Generate motion
    generator = HawaiiMotionGenerator()
    motion_params = config.get(args.type, {})
    
    motion_content = generator.generate_motion(args.type, motion_params)
    
    # Save motion
    filename = f"motion_{args.type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex"
    tex_file = generator.save_motion(motion_content, filename)
    
    print(f"Motion generated: {tex_file}")
    
    # Compile to PDF if requested
    if args.compile:
        pdf_file = generator.compile_latex(tex_file)
        print(f"PDF compiled: {pdf_file}")
        
if __name__ == "__main__":
    main()