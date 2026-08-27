using System;
using System.Diagnostics;
using System.IO;
using UiPath.CodedWorkflows;
using UiPath.Core;

namespace TestAutomationFramework.TestFramework.VideoRecording
{
    public class StartRecording : CodedWorkflow
    {
        [Workflow]
        public (Process out_ffmpegProcess, String out_VideoFilePath) Execute(String in_TestName, Boolean in_startRecording)
        {
            Log("StartRecording - Start");

            Process out_ffmpegProcess = null;
            string out_VideoFilePath = string.Empty;

            if (in_startRecording)
            {
                string fileUniqueName = in_TestName + "_" + Guid.NewGuid().ToString();
                out_VideoFilePath = Path.Combine(Path.GetTempPath(), fileUniqueName + ".webm");

                string perMachineFFmpegPath = Path.Combine(
                    Environment.GetEnvironmentVariable("ProgramFiles"),
                    @"UiPath\Studio\ffmpeg\ffmpeg.exe");

                string ffmpegExePath = string.Empty;

                if (File.Exists(perMachineFFmpegPath))
                {
                    ffmpegExePath = perMachineFFmpegPath;
                    Log("StartRecording - Found ffmpeg at: " + ffmpegExePath);
                }
                else
                {
                    string userFFmpegPath = Path.Combine(
                        Environment.GetEnvironmentVariable("LocalAppData"),
                        @"Programs\UiPath\Studio\ffmpeg\ffmpeg.exe");

                    if (File.Exists(userFFmpegPath))
                    {
                        ffmpegExePath = userFFmpegPath;
                        Log("StartRecording - Found ffmpeg at: " + ffmpegExePath);
                    }
                    else
                    {
                        Log("StartRecording - Could not find ffmpeg", LogLevel.Error);
                    }
                }

                if (!string.IsNullOrEmpty(ffmpegExePath))
                {
                    string cmd = "-probesize 500M -analyzeduration 1000 -f gdigrab -framerate 4 -thread_queue_size 32 " +
                                 "-i desktop -vf \"scale=iw*0.71:ih*0.71\" -c:v libvpx -crf 50 -b:v 1M " +
                                 "-force_key_frames \"expr:gte(t,n_forced*10)\" -deadline realtime -cpu-used 8 " +
                                 "-pix_fmt yuv420p -y \"" + out_VideoFilePath + "\"";

                    var startInfo = new ProcessStartInfo
                    {
                        FileName = ffmpegExePath,
                        Arguments = cmd,
                        UseShellExecute = false,
                        CreateNoWindow = true,
                        RedirectStandardInput = true
                    };

                    out_ffmpegProcess = new Process { StartInfo = startInfo };
                    out_ffmpegProcess.Start();
                    Log("StartRecording - Video recording started");
                }
            }
            else
            {
                Log("StartRecording - Recording not active, skipping");
            }

            return (out_ffmpegProcess, out_VideoFilePath);
        }
    }
}
