using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
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

namespace REFramework_CrossPlatform_CSharp
{
    public class NTakeScreenshot_Coded : CodedWorkflow
    {
        // Screenshot path provided as input will be suffixed with a timestamp
        [Workflow]
        public string Execute(string in_ScreenshotPath, int in_TimeoutMS = 15000)
        {
            try 
            {
                if(string.IsNullOrEmpty(in_ScreenshotPath))
                {
                    throw new ArgumentException("Expected valid screenshot path");
                }
                
                string newFilePath = SuffixWithTimestamp(in_ScreenshotPath);
                if(string.IsNullOrEmpty(newFilePath))
                {
                    throw new BusinessRuleException("Could not compute timestamped screenshot name.");
                }
                
                string screenshot = TakeDesktopScreenshot(in_TimeoutMS);
                if(string.IsNullOrEmpty(screenshot))
                {
                    throw new BusinessRuleException("Screenshot came as empty.");
                }
                
                SaveScreenshot(screenshot, newFilePath);
                return newFilePath;
            }
            catch (Exception ex)
            {
                Log(ex.Message);
                throw(ex); // Or what
            }
        }
        
        private string SuffixWithTimestamp(string imagePath)
        {
            string stamp = DateTime.Now.ToString("yyyy-MM-dd_HHmmss_fff");
            string directory = Path.GetDirectoryName(imagePath);
            string newFileName = $"{Path.GetFileNameWithoutExtension(imagePath)}_{stamp}{Path.GetExtension(imagePath)}";
            return string.IsNullOrEmpty(directory) ? newFileName : Path.Combine(directory, newFileName);
        }
        
        private string TakeDesktopScreenshot(int timeoutMs)
        {
            var target = UiPath.UiFactory.Instance.NewUiNode().FromDesktop();
            var options = UiPath.UiFactory.Instance.NewUiScreenshotOptions(UiPath.UiScreenshotFormat.ScreenshotFormatPng, UiPath.UiScreenshotCaptureMode.ScreenshotCaptureModeScreenArea, timeoutMs);
            var screenshotResponse = target.TakeScreenshot(options);
            return screenshotResponse.base64Screenshot;
        }
        
        private void SaveScreenshot(string screenshot, string path)
        {
            byte[] bytes = Convert.FromBase64String(screenshot);
            File.WriteAllBytes(path, bytes);
        }
    }
}