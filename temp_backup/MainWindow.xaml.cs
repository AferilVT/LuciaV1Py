using System;
using System.Diagnostics;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using System.Windows.Forms;
using System.Windows.Input;
using System.Runtime.InteropServices;
using System.Windows.Interop;
using System.Windows.Documents;

namespace LuciaBotLauncher
{
    public partial class MainWindow : Window
    {
        private Process? botProcess;
        private CancellationTokenSource? cancellationTokenSource;
        private System.Windows.Forms.NotifyIcon? trayIcon;
        private bool isMinimizedToTray;

        public MainWindow()
        {
            InitializeComponent();
            InitializeTrayIcon();
            // Set true rounded corners
            var hwnd = new WindowInteropHelper(this).Handle;
            int radius = 16;
            var rgn = WindowHelper.CreateRoundRectRgn(0, 0, (int)Width, (int)Height, radius, radius);
            WindowHelper.SetWindowRgn(hwnd, rgn, true);
            WindowHelper.DeleteObject(rgn);
        }

        private void InitializeTrayIcon()
        {
            trayIcon = new NotifyIcon
            {
                Icon = System.Drawing.Icon.ExtractAssociatedIcon(System.Reflection.Assembly.GetExecutingAssembly().Location),
                Visible = false,
                Text = "Lucia Bot Launcher"
            };

            var contextMenu = new System.Windows.Forms.ContextMenuStrip();
            var restoreItem = new System.Windows.Forms.ToolStripMenuItem("Restore", null, (s, e) => RestoreWindow());
            var exitItem = new System.Windows.Forms.ToolStripMenuItem("Exit", null, (s, e) => ExitApplication());
            contextMenu.Items.Add(restoreItem);
            contextMenu.Items.Add(exitItem);
            trayIcon.ContextMenuStrip = contextMenu;
            trayIcon.DoubleClick += (s, e) => RestoreWindow();
        }

        private async void StartButton_Click(object sender, RoutedEventArgs e)
        {
            if (botProcess != null && !botProcess.HasExited)
            {
                System.Windows.MessageBox.Show("Bot is already running.", "Info", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            ClearLog();
            StartButton.IsEnabled = false;
            StopButton.IsEnabled = true;
            UpdateStatus("Running", "#4CAF50");

            string pythonPath = FindPythonPath();
            if (string.IsNullOrEmpty(pythonPath))
            {
                System.Windows.MessageBox.Show("Python executable not found in PATH!", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            LogMessage($"Using Python: {pythonPath}\n");

            string projectRoot = Directory.GetParent(AppDomain.CurrentDomain.BaseDirectory)!.Parent!.Parent!.Parent!.FullName;
            string mainPyPath = Path.Combine(projectRoot, "src", "main.py");
            if (!File.Exists(mainPyPath))
            {
                System.Windows.MessageBox.Show($"Could not find main.py at {mainPyPath}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            var startInfo = new ProcessStartInfo
            {
                FileName = pythonPath,
                Arguments = $"\"{mainPyPath}\"",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                WorkingDirectory = Path.GetDirectoryName(mainPyPath)
            };

            botProcess = new Process { StartInfo = startInfo };
            cancellationTokenSource = new CancellationTokenSource();

            try
            {
                botProcess.Start();
                await ReadOutputAsync(cancellationTokenSource.Token);
            }
            catch (Exception ex)
            {
                LogMessage($"Error: {ex.Message}\n");
                StopBot();
            }
        }

        private void StopButton_Click(object sender, RoutedEventArgs e)
        {
            StopBot();
        }

        private void StopBot()
        {
            if (botProcess != null && !botProcess.HasExited)
            {
                botProcess.Kill();
                botProcess.WaitForExit();
            }

            cancellationTokenSource?.Cancel();
            StartButton.IsEnabled = true;
            StopButton.IsEnabled = false;
            UpdateStatus("Stopped", "#F44336");
            LogMessage("Bot stopped.\n");
        }

        private void ClearButton_Click(object sender, RoutedEventArgs e)
        {
            ClearLog();
        }

        private void ClearLog()
        {
            LogArea.Document.Blocks.Clear();
        }

        private async Task ReadOutputAsync(CancellationToken cancellationToken)
        {
            try
            {
                while (!cancellationToken.IsCancellationRequested)
                {
                    string line = await botProcess.StandardOutput.ReadLineAsync();
                    if (line == null) break;
                    
                    Dispatcher.Invoke(() => LogMessage(line + "\n"));
                }
            }
            catch (OperationCanceledException)
            {
                // Normal cancellation, do nothing
            }
            finally
            {
                Dispatcher.Invoke(() =>
                {
                    StartButton.IsEnabled = true;
                    StopButton.IsEnabled = false;
                    UpdateStatus("Stopped", "#F44336");
                });
            }
        }

        private void LogMessage(string message)
        {
            LogArea.Dispatcher.Invoke(() =>
            {
                LogArea.IsReadOnly = false;
                foreach (var line in message.Split('\n'))
                {
                    if (string.IsNullOrWhiteSpace(line)) continue;
                    var paragraph = new Paragraph();
                    var run = new Run(line + "\n");
                    if (line.Contains("[USER]"))
                        run.Foreground = new SolidColorBrush(Color.FromRgb(0, 255, 255)); // Cyan
                    else if (line.Contains("[API]"))
                        run.Foreground = new SolidColorBrush(Color.FromRgb(255, 165, 0)); // Orange
                    else if (line.Contains("[ERROR]"))
                        run.Foreground = new SolidColorBrush(Color.FromRgb(255, 80, 80)); // Red
                    else
                        run.Foreground = new SolidColorBrush(Color.FromRgb(238, 238, 238)); // Default
                    paragraph.Inlines.Add(run);
                    LogArea.Document.Blocks.Add(paragraph);
                }
                LogArea.ScrollToEnd();
                LogArea.IsReadOnly = true;
            });
        }

        private void UpdateStatus(string status, string color)
        {
            StatusText.Text = $"Status: {status}";
            StatusText.Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString(color));
        }

        private string FindPythonPath()
        {
            string[] possiblePaths = new[]
            {
                "python",
                "python3",
                @"C:\Python39\python.exe",
                @"C:\Python310\python.exe",
                @"C:\Python311\python.exe"
            };

            foreach (string path in possiblePaths)
            {
                try
                {
                    var process = Process.Start(new ProcessStartInfo
                    {
                        FileName = path,
                        Arguments = "--version",
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        CreateNoWindow = true
                    });

                    if (process != null)
                    {
                        process.WaitForExit();
                        if (process.ExitCode == 0)
                        {
                            return path;
                        }
                    }
                }
                catch
                {
                    continue;
                }
            }

            return null;
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (botProcess != null && !botProcess.HasExited)
            {
                var result = System.Windows.MessageBox.Show(
                    "Bot is still running. Do you want to stop it and exit?",
                    "Quit",
                    MessageBoxButton.YesNo,
                    MessageBoxImage.Question);

                if (result == MessageBoxResult.No)
                {
                    e.Cancel = true;
                    MinimizeToTray();
                    return;
                }

                StopBot();
            }

            trayIcon.Visible = false;
            trayIcon.Dispose();
        }

        private void MinimizeToTray()
        {
            if (isMinimizedToTray) return;

            Hide();
            trayIcon.Visible = true;
            isMinimizedToTray = true;
        }

        private void RestoreWindow()
        {
            Show();
            WindowState = WindowState.Normal;
            Activate();
            trayIcon.Visible = false;
            isMinimizedToTray = false;
        }

        private void ExitApplication()
        {
            if (botProcess != null && !botProcess.HasExited)
            {
                StopBot();
            }
            Close();
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private void TitleBar_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ButtonState == MouseButtonState.Pressed)
                this.DragMove();

        }

        protected override void OnRenderSizeChanged(SizeChangedInfo sizeInfo)
        {
            base.OnRenderSizeChanged(sizeInfo);
            var hwnd = new WindowInteropHelper(this).Handle;
            int radius = 16;
            var rgn = WindowHelper.CreateRoundRectRgn(0, 0, (int)ActualWidth, (int)ActualHeight, radius, radius);
            WindowHelper.SetWindowRgn(hwnd, rgn, true);
            WindowHelper.DeleteObject(rgn);
        }
    }

    // Win32 interop for rounded corners
    public static class WindowHelper
    {
        [DllImport("gdi32.dll")]
        public static extern IntPtr CreateRoundRectRgn(
            int nLeftRect, int nTopRect, int nRightRect, int nBottomRect, int nWidthEllipse, int nHeightEllipse);

        [DllImport("user32.dll")]
        public static extern int SetWindowRgn(IntPtr hWnd, IntPtr hRgn, bool bRedraw);

        [DllImport("gdi32.dll")]
        public static extern bool DeleteObject(IntPtr hObject);
    }
} 