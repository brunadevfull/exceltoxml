# Conversor Excel → XML - Sistema Banco do Brasil

## Overview

This is a desktop application for converting Excel spreadsheets to XML files in the specific format required by Banco do Brasil's payment command system. The application is built with Python and Tkinter, providing a native desktop interface that works across Windows, Linux, and macOS.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Tkinter (Python's built-in GUI library)
- **Pattern**: MVC-like structure with separation of concerns
- **Components**: 
  - Main window with 70% content area and 30% sidebar
  - Custom widgets for file drag-and-drop functionality
  - Responsive layout with proper grid management
  - Native desktop feel with platform-specific styling

### Backend Architecture
- **Language**: Python 3.x
- **Structure**: Modular service-oriented architecture
- **Services**: 
  - Excel processor for reading and validating spreadsheet data
  - XML generator for creating BB-formatted payment commands
  - Data manager for persistent storage of configuration and responsible persons
- **Models**: Simple dataclass-based models for data representation

### Data Storage Solutions
- **Configuration**: JSON files stored in OS-appropriate directories
  - Windows: `%APPDATA%/ConversorExcelXML`
  - macOS: `~/Library/Application Support/ConversorExcelXML`
  - Linux: `~/.config/conversorexcelxml`
- **Backup**: Automatic backup system for configuration files
- **No Database**: Uses file-based storage for simplicity and portability

## Key Components

### 1. Main Application (`main.py`)
- Application entry point and window management
- Handles window centering and basic configuration
- Initializes core services and GUI components

### 2. GUI Components (`src/gui/`)
- **MainWindow**: Primary interface controller
- **Widgets**: Custom components including file drop area
- **Styling**: Centralized styling system with color schemes and fonts

### 3. Data Models (`src/models/`)
- **Responsible**: Dataclass for managing responsible person information
- Includes validation and serialization methods
- Supports conversion to/from dictionary format

### 4. Services (`src/services/`)
- **DataManager**: Handles persistent storage and configuration
- **ExcelProcessor**: Reads and validates Excel files using pandas
- **XMLGenerator**: Creates XML output in BB-specific format

### 5. Utilities (`src/utils/`)
- **Validators**: CPF validation using Brazilian algorithm, folha format validation
- **Constants**: Application-wide constants and configuration values

## Data Flow

1. **File Selection**: User selects Excel file via drag-and-drop or file dialog
2. **Data Processing**: Excel file is read and validated using pandas
3. **Responsible Selection**: User selects or creates responsible person data
4. **XML Generation**: Processed data is converted to BB XML format
5. **File Output**: Generated XML is saved to user-specified location

### Processing Pipeline
- Excel → DataFrame → Validation → Record Processing → XML Generation
- Error handling at each step with user-friendly messages
- Progress tracking for large files

## External Dependencies

### Core Libraries
- **pandas**: Excel file reading and data manipulation
- **openpyxl**: Excel file handling and formatting
- **tkinter**: GUI framework (built-in with Python)
- **pathlib**: Modern path handling
- **xml.etree.ElementTree**: XML generation
- **json**: Configuration file handling

### File Format Support
- **Input**: .xlsx, .xls (Excel formats)
- **Output**: .xml (BB-specific format with iso-8859-1 encoding)

## Deployment Strategy

### Distribution
- **Standalone Application**: Single executable using PyInstaller or similar
- **Cross-Platform**: Same codebase works on Windows, Linux, and macOS
- **No Installation Required**: Portable application approach
- **Configuration Persistence**: Uses OS-appropriate config directories

### Requirements
- Python 3.x runtime (if not using compiled executable)
- Minimal system requirements for desktop GUI
- No network connectivity required (fully offline operation)

### Key Features
- **Drag-and-Drop Interface**: User-friendly file selection
- **Responsible Person Management**: Persistent storage of user data
- **Data Validation**: Comprehensive validation of Excel data and CPF
- **XML Generation**: BB-specific format with proper encoding
- **Error Handling**: User-friendly error messages and validation feedback
- **Progress Tracking**: Visual feedback during processing
- **Backup System**: Automatic configuration backups

The application follows a clean architecture with clear separation between GUI, business logic, and data management layers, making it maintainable and extensible for future requirements.