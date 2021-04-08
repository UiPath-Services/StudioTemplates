# Studio Templates

Studio Templates is a place where we keep our REFramework templates. 

## Installation

They should always be in the latest version of Studio. 
Otherwise, you can simply clone this repo and use the templates from here.

## Usage

Remember: A "Template" project cannot be uploaded to Orchestrator. 

If you cloned this repository (instead of using the template from Studio):
1. Open the nuget that comes with the template
2. Otherwise, copy the project into a new *process* and don't use the *template* you cloned. It is not a normal *process*.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

#### *Do not push directly to master/develop!* Create pull requests for that. You will need at least one approval. 

- Any new features will be created in a feature/<your_target_package>/<your_feature_name> branch ex: "feature/du/remove_dependencies"
- Any new bugfix will be created in a bugfix/<your_target_package>/<your_bug_name> branch ex: "bugfix/ref/fixed_open_issue_1234"
- develop will always be the main branch that is the most up to date
- the 'master' branches will be the release channels for the different projects that we have 
Ex: When we release a new update of Document Understanding Process, it will be published in master/DocumentUnderstandingProcess) from there it will be built and pushed to the official feed in Studio

## License
Mixed. See each project individually.
