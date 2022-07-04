using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Diagnostics;
using System.Net.Http;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Text.Json;

namespace talkWithGakugeiChan
{
    public class Receiver
    {
        public string? msg { get; set; }
        public string? emt { get; set; }
    }
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private static HttpClient client = new HttpClient();
        public MainWindow()
        {
            InitializeComponent();
        }
        private void Window_ContentRendered(object sender, EventArgs e)
        {
            MediaVideo.LoadedBehavior = MediaState.Stop;
            MediaVideo.Visibility = Visibility.Hidden;
            MediaVideo.Source = new Uri(@"wtg.mp4", UriKind.Relative);
            MediaVideo.Position = TimeSpan.Zero;
            MediaVideo.Visibility = Visibility.Visible;
            MediaVideo.LoadedBehavior = MediaState.Manual;
            MediaVideo.MediaEnded += (sender, e) =>
            {
                MediaVideo.Position = TimeSpan.FromMilliseconds(0);
                MediaVideo.Play();
            };
            MediaVideo.Play();
            
            // 動画ファイルをロードします。
            
        }

        private void TextBox_TextChanged(object sender, TextChangedEventArgs e)
        {

        }

        private async void Button_Click(object sender, RoutedEventArgs e)
        {
            Answer.Text = "考え中……";

           

            Debug.Print(InputBox.Text);
            string url = "http://127.0.0.1:8000/";
            var dic = new Dictionary<string, string>()
            {
                { "msg",InputBox.Text}
            };

            var jsonstr = JsonSerializer.Serialize(dic);
            var content = new StringContent(jsonstr, Encoding.UTF8, "application/json");
            Debug.Print(jsonstr);
            HttpResponseMessage responseMessage;
            try
            {
                
                responseMessage = await client.PostAsync(url, content);
                var json = await responseMessage.Content.ReadAsStringAsync();
                Debug.Write(json); 

                Receiver data = JsonSerializer.Deserialize<Receiver>(json);
                Debug.Write(data);
                var msg = data.msg;
                var emt = data.emt;
                Debug.Write(msg);
                Debug.Write(emt);
                Answer.Text = msg;
                if (emt.Equals("banzai")){
                    MediaVideo.LoadedBehavior = MediaState.Stop;
                    MediaVideo.Visibility = Visibility.Hidden;
                    MediaVideo.Source = new Uri(@"bnzi.mp4", UriKind.Relative);
                    MediaVideo.Position = TimeSpan.Zero;
                    MediaVideo.Visibility = Visibility.Visible;
                    MediaVideo.LoadedBehavior = MediaState.Manual;
                    MediaVideo.MediaEnded += (sender, e) =>
                    {
                        MediaVideo.Source = new Uri(@"wtg.mp4", UriKind.Relative);
                        MediaVideo.Position = TimeSpan.Zero;
                        MediaVideo.Position = TimeSpan.FromMilliseconds(0);
                        MediaVideo.Play();
                        MediaVideo.MediaEnded += (sender, e) =>
                        {
                            MediaVideo.Position = TimeSpan.FromMilliseconds(0);
                            MediaVideo.Play();
                        };
                        MediaVideo.Play();

                    };
                    MediaVideo.Play();
                }
                if (emt.Equals("yatta"))
                {
                    MediaVideo.LoadedBehavior = MediaState.Stop;
                    MediaVideo.Visibility = Visibility.Hidden;
                    MediaVideo.Source = new Uri(@"yorokobu.mp4", UriKind.Relative);
                    MediaVideo.Position = TimeSpan.Zero;
                    MediaVideo.Visibility = Visibility.Visible;
                    MediaVideo.LoadedBehavior = MediaState.Manual;
                    MediaVideo.MediaEnded += (sender, e) =>
                    {
                        MediaVideo.Source = new Uri(@"wtg.mp4", UriKind.Relative);
                        MediaVideo.Position = TimeSpan.Zero;
                        MediaVideo.Position = TimeSpan.FromMilliseconds(0);
                        MediaVideo.MediaEnded += (sender, e) =>
                        {
                            MediaVideo.Position = TimeSpan.FromMilliseconds(0);
                            MediaVideo.Play();
                        };
                        MediaVideo.Play();
                    };
                    MediaVideo.Play();
                }
                if (emt.Equals("oko"))
                {
                    MediaVideo.LoadedBehavior = MediaState.Stop;
                    MediaVideo.Visibility = Visibility.Hidden;
                    MediaVideo.Source = new Uri(@"ok.mp4", UriKind.Relative);
                    MediaVideo.Position = TimeSpan.Zero;
                    MediaVideo.Visibility = Visibility.Visible;
                    MediaVideo.LoadedBehavior = MediaState.Manual;
                    MediaVideo.MediaEnded += (sender, e) =>
                    {
                        MediaVideo.Source = new Uri(@"wtg.mp4", UriKind.Relative);
                        MediaVideo.Position = TimeSpan.Zero;
                        MediaVideo.Position = TimeSpan.FromMilliseconds(0);
                        MediaVideo.MediaEnded += (sender, e) =>
                        {
                            MediaVideo.Position = TimeSpan.FromMilliseconds(0);
                            MediaVideo.Play();
                        };
                        MediaVideo.Play();
                    };
                    MediaVideo.Play();
                }
                else
                {
                    MediaVideo.LoadedBehavior = MediaState.Stop;
                    MediaVideo.Visibility = Visibility.Hidden;
                    MediaVideo.Source = new Uri(@"un.mp4", UriKind.Relative);
                    MediaVideo.Position = TimeSpan.Zero;
                    MediaVideo.Visibility = Visibility.Visible;
                    MediaVideo.LoadedBehavior = MediaState.Manual;
                    MediaVideo.MediaEnded += (sender, e) =>
                    {
                        MediaVideo.Source = new Uri(@"wtg.mp4", UriKind.Relative);
                        MediaVideo.Position = TimeSpan.Zero;
                        MediaVideo.Position = TimeSpan.FromMilliseconds(0);
                        MediaVideo.MediaEnded += (sender, e) =>
                        {
                            MediaVideo.Position = TimeSpan.FromMilliseconds(0);
                            MediaVideo.Play();
                        };
                        MediaVideo.Play();
                    };
                    MediaVideo.Play();
                }

            }
            catch
            {
                return;
            }
        }

    }
}
