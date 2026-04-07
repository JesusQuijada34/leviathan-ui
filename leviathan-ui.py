#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
leviathan-ui - CLI Entry Point v1.0.5
SetupDialogs - Sistema de instaladores profesionales
"""

import sys
from pathlib import Path

# Añadir directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent))

from leviathan_ui.cli import main

if __name__ == '__main__':
    sys.exit(main())

