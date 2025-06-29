# File Transfer Application

A client-server file transfer application built with Python and Tkinter GUI for university coursework.

## 📋 Project Information

- **University**: Vietnam National University Ho Chi Minh City - University of Science (VNU-HCMUS)
- **Semester**: 3rd Semester
- **Course**: Computer Networks
- **Project Type**: Team Project
- **Language**: Python
- **GUI Framework**: Tkinter

## 📖 Description

This is a comprehensive file transfer application that allows users to upload, download, delete, and rename files between a client and server over a TCP connection. The application features a modern graphical user interface with file type icons and an intuitive design.

## ✨ Features

### Client Features
- **Modern GUI Interface**: Clean and user-friendly interface built with Tkinter
- **File Upload**: Upload files from client to server
- **File Download**: Download files from server to client
- **File Management**: Delete and rename files on the server
- **File Type Icons**: Visual representation of different file types (PDF, DOCX, MP3, MP4, ZIP, etc.)
- **Connection Management**: Connect/disconnect from server with custom IP and port

### Server Features
- **Multi-client Support**: Handle multiple clients simultaneously using threading
- **File Storage**: Secure file storage in dedicated server directory
- **Request Handling**: Process upload, download, delete, and rename requests
- **Error Handling**: Comprehensive error handling and logging

### Technical Features
- **TCP Socket Communication**: Reliable file transfer using TCP protocol
- **Chunked File Transfer**: Efficient transfer of large files using chunking
- **Multi-threading**: Concurrent file operations for better performance
- **Error Recovery**: Robust error handling and recovery mechanisms

## 🏗️ Project Structure

```
file-transfer/
├── client/
│   ├── client.py          # Client class with file operations
│   ├── file_transfer.py   # File transfer utilities
│   ├── gui.py            # Tkinter GUI implementation
│   └── source/           # GUI assets and icons
│       ├── bg2.png
│       ├── docx.png
│       ├── log_in.png
│       └── ... (other icons)
├── server/
│   ├── server.py         # Server class with request handling
│   ├── file_transfer.py  # File transfer utilities
│   └── server_data/      # Server file storage directory
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Tkinter (usually comes with Python)
- Socket library (built-in)
- Threading library (built-in)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd file-transfer
   ```

2. **No additional dependencies required** - The project uses only Python standard libraries

### Running the Application

#### Starting the Server

1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Run the server:
   ```bash
   python server.py
   ```

3. The server will start listening on your local IP address on port 9999 by default

#### Starting the Client

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Run the client:
   ```bash
   python gui.py
   ```

3. Enter server IP and port in the login interface
4. Click connect to establish connection with the server

## 🎮 Usage

### Connecting to Server

1. Launch the client application
2. Enter the server IP address (default: localhost)
3. Enter the server port (default: 9999)
4. Click "Connect" to establish connection

### File Operations

- **Upload**: Select files from your local system to upload to server
- **Download**: Browse server files and download to your local system
- **Delete**: Remove files from the server
- **Rename**: Change file names on the server

## 🔧 Configuration

### Server Configuration

- **Port**: Default port is 9999 (can be modified in `server.py`)
- **Buffer Size**: Default buffer size is ~100MB (can be adjusted)
- **Storage Directory**: Files are stored in `server/server_data/`

### Client Configuration

- **Server IP**: Configurable through GUI (default: localhost)
- **Server Port**: Configurable through GUI (default: 9999)
- **Download Directory**: Files downloaded to `client_data/`

## 🛠️ Technical Details

### Protocol

The application uses a custom protocol over TCP:
- `REQ@SND@filename` - Upload request
- `REQ@DWN@filename` - Download request  
- `REQ@DEL@filename` - Delete request
- `REQ@REN@oldname@newname` - Rename request

### File Transfer

- Files are transferred in chunks for efficient memory usage
- Multi-threading is used for concurrent chunk processing
- Error checking ensures file integrity

## 🤝 Contributing

This is a university project, but contributions and suggestions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is for educational purposes as part of university coursework.

## 👥 Team Members
- @xing215
- @TrucmaiUS
- @nickhuy1809

---

*This project was developed as part of the 3rd semester coursework at VNU-HCMUS.*
