# restain_app


use USB2000PLUS or HR2000PLUS

set up.

Versions tested on
 Python 3.9.13 
Python 3.11.4

to install required libraries run install script

legacy files are in place in case someone wants to use a different spectrometer, if thor labs one is used can centeralize to one file to avoid seperate files access same dlls and folder 


## Main.py
The provided code defines a Python application for controlling a spectrometer and an LED driver, collecting light and dark samples, and saving measurement data. The application uses the Tkinter library to create a graphical user interface (GUI) that allows users to interact with the hardware and manage data collection.

At the top, the code imports necessary modules, including Tkinter for the GUI, NumPy for numerical operations, CSV for data storage, and Matplotlib for plotting. It also imports custom modules for spectrometer and LED control, as well as GUI components.

The main class, resistain_app, encapsulates all application logic. In its constructor (__init__), it initializes various attributes related to the spectrometer, LED driver, sample data, configuration, and file management. It ensures that a data directory exists for storing measurement files.

The startApp method sets up the main Tkinter window, configures its properties, and initializes the GUI by calling buildGUI. The GUI includes buttons for taking dark and light samples and saving data, as well as labels for displaying process status and dark room status. When the GUI is built, the application loads the spectrometer configuration from a JSON file, creating a default one if necessary, and initializes the spectrometer and LED driver.

The methods take_dark and take_light handle the process of collecting dark and light samples, respectively. They interact with the hardware, perform averaging and smoothing of the collected data, and update the GUI to reflect the current status. The graph method visualizes the difference between light and dark samples using Matplotlib.

For data management, the get_sample_num method determines the next available sample number based on existing files, ensuring unique filenames for each measurement. The save method writes the collected data to a CSV file, including wavelength, light, dark, and normalized values.

Error handling is managed by the status_check method, which ensures that both the spectrometer and LED driver are operational, reloading them if necessary. The application is started by creating an instance of resistain_app and calling its startApp method when the script is run directly.

Overall, the code demonstrates a structured approach to integrating hardware control, data acquisition, and user interaction in a scientific measurement application.

## gui.py
This code defines a set of reusable, object-oriented GUI components for a Tkinter-based Python application, with a focus on consistent styling and easy management of widget instances. The module starts by importing necessary libraries, including Tkinter, PIL for image handling, and standard modules like os and sys. The resource_path function is a utility that helps locate resource files (like images) in both development and packaged (e.g., PyInstaller) environments.

The TkImage class wraps image loading and caching, allowing images to be referenced by a string key and reused across the application. It tries to load an image from a given path, handling both normal and packaged execution contexts.

Several custom widget classes are defined, each inheriting from a standard Tkinter widget (like Label, Button, Entry, etc.). Each class maintains a dictionary of its instances, keyed by a reference string, which allows for easy access and removal of widgets by name. For example, the Label and Button classes provide a remove class method to destroy either a specific widget or all widgets of that type.

Specialized subclasses like StandardLabel, StandardButtons, and StandardInput apply a consistent flat, borderless style and other visual tweaks to their respective widgets. The ToggleButton and TabButton classes add toggleable behavior, changing their appearance based on state, and are designed to work with images for visual feedback.

Other components include Input (a styled entry field), Scale (a styled slider), dropdown (a styled combo box), and CheckBox (a styled checkbutton). Each of these classes follows the same pattern of instance management and style customization, making it easier to build and maintain a visually consistent and easily controllable GUI.

Overall, this module abstracts away much of the repetitive setup and management code required for Tkinter widgets, promoting code reuse and maintainability in larger GUI applications.

## led_controller.py
This code defines a Python class, dc2200, which provides an interface for controlling a Thorlabs DC2200 LED driver via its vendor-supplied DLL. The class uses the ctypes library to interact with the DLL, allowing Python code to call functions written in C for hardware control.

In the constructor (__init__), the class initializes several attributes, including the path to the DLL, the device resource string, and variables to track the device state, error messages, and current settings. The init_driver method loads the DLL, initializes the device session, and sets the LED driver to constant current mode with the LED initially turned off. If initialization fails, it retrieves and stores an error message from the DLL.

The on method turns the LED on at a specified current (default 2 Amps), sets the device state, and waits briefly to allow the hardware to respond. It then queries the actual current applied to the LED and calculates the percentage error between the requested and measured current, storing this value for later inspection.

The off method turns the LED off and updates the internal state. The toggle method switches the LED on or off depending on its current state, using the specified current when turning on. The quit method ensures the LED is turned off and closes the device session cleanly.

Overall, this class abstracts the low-level details of DLL interaction and device communication, providing a simple Pythonic interface for higher-level application code to control the LED driver safely and reliably.

## spec controller 
This code defines the oceanoptic_controller class, which provides a Python interface for controlling and acquiring data from an Ocean Optics spectrometer using the seabreeze library. The class is designed to simplify spectrometer initialization, data acquisition, and resource management for scientific or industrial applications.

In the constructor (__init__), the class sets up key parameters such as the integration time (how long the spectrometer collects light for each measurement) and the spectrometer model. It also initializes status flags and placeholders for wavelength and intensity data.

The init_spec method is responsible for detecting connected spectrometers and initializing the first available device. It uses list_devices() to find all connected Ocean Optics spectrometers. If no devices are found, it sets the status to False. Otherwise, it opens the first available spectrometer, sets its integration time, and marks the status as True. There is commented-out code that suggests an alternative approach for selecting a spectrometer by model name, but the current implementation always uses the first detected device.

The get_spectra method retrieves spectral data from the spectrometer. If the device is not initialized (status is False), it attempts to re-initialize it. If successful, it fetches the wavelength and intensity arrays from the device and stores them in the object's attributes. If any error occurs during this process, the status is set to False to indicate a problem.

Finally, the quit method closes the connection to the spectrometer, releasing any resources held by the device. This is important for ensuring that the hardware is properly released and can be accessed by other processes or future runs of the program.

Overall, this class abstracts away the low-level details of device management, providing a simple and reusable interface for spectrometer operations in Python.
