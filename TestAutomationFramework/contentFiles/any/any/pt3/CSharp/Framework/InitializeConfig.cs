using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text.Json;
using UiPath.CodedWorkflows;

namespace TestAutomationFrameworkCS
{
    /// <summary>
    /// Loads Config\Settings.json, Config\Constants.json and Config\Assets.json into one dictionary,
    /// keyed by each entry's Name. Settings and constants hold text values (an empty or missing Value is
    /// an empty string, as REFramework reads its Config.xlsx); an asset holds the
    /// Orchestrator asset value, a credential holds a NetworkCredential (user name and SecurePassword).
    /// TestTimeout (required) and TearDownTimeout (optional) are settings stored as TimeSpan.
    /// TestName is reserved: the execution template adds it from the current job.
    /// Every failure surfaces as one exception whose message names the file, the entry and what is allowed.
    /// </summary>
    public class InitializeConfig : CodedWorkflow
    {
        private const string ConfigFolder = "Config";
        private const string AssetsFile = "Assets.json";
        private const string ExamplePrefix = "example_";
        private static readonly string[] ReservedNames = { "TestName" };
        private static readonly string[] AssetTypes = { "Asset", "Credential" };

        [Workflow]
        public Dictionary<string, object> Execute()
        {
            var config = new Dictionary<string, object>();
            var settingValues = new Dictionary<string, string>();

            var settings = new List<string>();
            foreach (var entry in ReadEntries("Settings.json"))
            {
                var name = ReadString(entry, "Settings.json", "Name");
                var value = ReadString(entry, "Settings.json", "Value", required: false);
                AddEntry(config, "Settings.json", name, value);
                settingValues[name] = value;
                settings.Add($"{name} = '{value}'");
            }
            Log($"InitializeConfig - Settings ({settings.Count}): {Describe(settings)}");

            var constants = new List<string>();
            foreach (var entry in ReadEntries("Constants.json"))
            {
                var name = ReadString(entry, "Constants.json", "Name");
                var value = ReadString(entry, "Constants.json", "Value", required: false);
                AddEntry(config, "Constants.json", name, value);
                constants.Add($"{name} = '{value}'");
            }
            Log($"InitializeConfig - Constants ({constants.Count}): {Describe(constants)}");

            // Asset values are never logged: a text asset can hold a secret and a credential always does.
            var assets = new List<string>();
            foreach (var entry in ReadEntries(AssetsFile))
            {
                var name = ReadString(entry, AssetsFile, "Name");
                var assetName = ReadString(entry, AssetsFile, "AssetName");
                var folder = ReadString(entry, AssetsFile, "Folder", required: false);
                var type = ReadAssetType(entry, name);
                AddEntry(config, AssetsFile, name, LoadAsset(name, assetName, folder, type));
                assets.Add($"{name} <- {type} '{assetName}' in {DescribeFolder(folder)}");
            }
            Log($"InitializeConfig - Assets ({assets.Count}): {Describe(assets)}");

            config["TestTimeout"] = ReadTimeout(settingValues, "TestTimeout", required: true);
            if (settingValues.ContainsKey("TearDownTimeout"))
            {
                config["TearDownTimeout"] = ReadTimeout(settingValues, "TearDownTimeout", required: false);
            }

            return config;
        }

        private static List<JsonElement> ReadEntries(string fileName)
        {
            var path = Path.Combine(Directory.GetCurrentDirectory(), ConfigFolder, fileName);
            if (!File.Exists(path))
            {
                throw new FileNotFoundException($"InitializeConfig - configuration file not found: {path}. {ConfigFolder}\\{fileName} must exist in the project and hold a JSON array of entries (use [] for none).", path);
            }

            string text;
            try
            {
                text = File.ReadAllText(path);
            }
            catch (Exception ex) when (ex is IOException || ex is UnauthorizedAccessException)
            {
                throw new InvalidOperationException($"InitializeConfig - {ConfigFolder}\\{fileName} could not be read ({ex.GetType().Name}). Check that the file is not locked and that the robot can read it.", ex);
            }

            JsonDocument document;
            try
            {
                document = JsonDocument.Parse(text);
            }
            catch (JsonException ex)
            {
                throw new ArgumentException($"InitializeConfig - {ConfigFolder}\\{fileName} is not valid JSON: {ex.Message}", ex);
            }

            using (document)
            {
                if (document.RootElement.ValueKind != JsonValueKind.Array)
                {
                    throw new ArgumentException($"InitializeConfig - {ConfigFolder}\\{fileName} must be a JSON array of entries.");
                }

                var entries = new List<JsonElement>();
                foreach (var entry in document.RootElement.EnumerateArray())
                {
                    if (entry.ValueKind != JsonValueKind.Object)
                    {
                        throw new ArgumentException($"InitializeConfig - every entry of {fileName} must be a JSON object.");
                    }
                    entries.Add(entry.Clone());
                }
                return entries;
            }
        }

        private static string ReadString(JsonElement entry, string fileName, string property, bool required = true)
        {
            if (!entry.TryGetProperty(property, out var value) || value.ValueKind == JsonValueKind.Null)
            {
                if (required)
                {
                    throw new ArgumentException($"InitializeConfig - an entry of {fileName} has no '{property}': {entry.GetRawText()}");
                }
                return string.Empty;
            }

            if (value.ValueKind != JsonValueKind.String)
            {
                throw new ArgumentException($"InitializeConfig - '{property}' must be a JSON string in {fileName}: {entry.GetRawText()}");
            }

            var text = value.GetString();
            if (required && string.IsNullOrWhiteSpace(text) && (property == "Name" || property == "AssetName"))
            {
                throw new ArgumentException($"InitializeConfig - an entry of {fileName} has an empty {property}: {entry.GetRawText()}");
            }
            return text;
        }

        // An empty or missing Type means Asset. The check runs before any asset is loaded.
        private static string ReadAssetType(JsonElement entry, string name)
        {
            var type = ReadString(entry, AssetsFile, "Type", required: false);
            if (string.IsNullOrEmpty(type))
            {
                return "Asset";
            }

            foreach (var allowed in AssetTypes)
            {
                if (type.Equals(allowed, StringComparison.OrdinalIgnoreCase))
                {
                    return allowed;
                }
            }

            throw new ArgumentException($"InitializeConfig - entry '{name}' in {AssetsFile} has Type '{type}'. Allowed values: {string.Join(", ", AssetTypes)} (empty means Asset).");
        }

        private static string Describe(List<string> items)
        {
            return items.Count == 0 ? "none" : string.Join("; ", items);
        }

        private static string DescribeFolder(string folder)
        {
            return string.IsNullOrWhiteSpace(folder) ? "the job's folder" : $"folder '{folder}'";
        }

        private static void AddEntry(Dictionary<string, object> config, string fileName, string name, object value)
        {
            if (Array.IndexOf(ReservedNames, name) >= 0)
            {
                throw new ArgumentException($"InitializeConfig - '{name}' in {fileName} is reserved: the execution template sets it from the current job.");
            }

            if (config.ContainsKey(name))
            {
                throw new ArgumentException($"InitializeConfig - '{name}' in {fileName} is already defined in another configuration file.");
            }
            config.Add(name, value);
        }

        private object LoadAsset(string name, string assetName, string folder, string type)
        {
            var folderPath = string.IsNullOrWhiteSpace(folder) ? null : folder;

            try
            {
                if (type == "Credential")
                {
                    var (userName, password) = system.GetCredential(assetName, folderPath);
                    return new NetworkCredential(userName, password);
                }

                return system.GetAsset(assetName, folderPath);
            }
            catch (Exception ex)
            {
                // The inner exception is kept for the details; its message is not repeated here.
                var expected = type == "Credential" ? "a Credential asset" : "a Text, Integer or Boolean asset";
                var example = name.StartsWith(ExamplePrefix, StringComparison.Ordinal)
                    ? $" '{name}' is an example entry: remove it from {AssetsFile} or create the asset."
                    : string.Empty;
                throw new InvalidOperationException(
                    $"InitializeConfig - Config entry '{name}' ({AssetsFile}) could not be loaded from Orchestrator asset '{assetName}' in {DescribeFolder(folder)}, expected {expected} ({ex.GetType().Name}). " +
                    $"Check that the asset exists in that folder, that the robot can access the folder, and that the asset type matches the entry (a Credential entry needs a Credential asset).{example} See the inner exception for details.",
                    ex);
            }
        }

        private static TimeSpan ReadTimeout(Dictionary<string, string> settings, string name, bool required)
        {
            if (!settings.TryGetValue(name, out var value))
            {
                throw new ArgumentException($"InitializeConfig - setting '{name}' is required in Settings.json (format hh:mm:ss, for example 00:20:00).");
            }

            // A bare number such as "20" is a valid "c" duration (20 days), so the colons are required explicitly.
            if (value.IndexOf(':') < 0 || !TimeSpan.TryParseExact(value, "c", CultureInfo.InvariantCulture, out var timeout) || timeout <= TimeSpan.Zero)
            {
                throw new ArgumentException($"InitializeConfig - setting '{name}' in Settings.json must be a positive duration in the format hh:mm:ss (for example 00:20:00), not '{value}'.");
            }
            return timeout;
        }
    }
}
