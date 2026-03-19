using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.IO;
using TestAutomationFramework.ObjectRepository;
using UiPath.Activities.System.Jobs.Coded;
using UiPath.CodedWorkflows;
using UiPath.Core;
using UiPath.Core.Activities.Storage;
using UiPath.Orchestrator.Client.Models;
using UiPath.Testing;
using UiPath.Testing.Activities.Api.Models;
using UiPath.Testing.Activities.Models;
using UiPath.Testing.Activities.TestData;
using UiPath.Testing.Activities.TestDataQueues.Enums;
using UiPath.Testing.Enums;
using UiPath.UIAutomationNext.API.Contracts;
using UiPath.UIAutomationNext.API.Models;
using UiPath.UIAutomationNext.Enums;

namespace TestAutomationFramework.TestFramework.VideoRecording
{
    public class StartRecording : CodedWorkflow
    {
        [Workflow]
        public (Process out_ffmpegProcess, string out_VideoFilePath) Execute(string in_TestName, bool in_startRecording)
        {
            Log("StartRecording");

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
                    Log("Found ffmpeg at: " + ffmpegExePath);
                }
                else
                {
                    string userFFmpegPath = Path.Combine(
                        Environment.GetEnvironmentVariable("LocalAppData"),
                        @"Programs\UiPath\Studio\ffmpeg\ffmpeg.exe");

                    if (File.Exists(userFFmpegPath))
                    {
                        ffmpegExePath = userFFmpegPath;
                        Log("Found ffmpeg at: " + ffmpegExePath);
                    }
                    else
                    {
                        Log("Could not find ffmpeg", LogLevel.Error);
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
                    Log("Video Recording started");
                }
            }
            else
            {
                Log("Recording not active. Skip video recording");
            }

            return (out_ffmpegProcess, out_VideoFilePath);
        }
    }
}