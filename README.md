## App Info Schema

A JSON schema for validating an `app_info.json` of a PLCnext Control App according to rules specified in the [official documentation](https://store.plcnext.help/st/PLCnext_App_Integration_Guide/Apps_parts/App_parts.htm).

The schema is built using [JSON Schema](https://json-schema.org/) draft `2020-12` and is tested within this repository.

## Usage

The schema file may be used in different ways.

### Code Editor

Many editors support schema files out of the box and allow validation and completions while editing a JSON file.

Therefore a `$schema` property can be added:

```json
{
    "$schema": "https://git-ima.europe.phoenixcontact.com/K06295/app-info-schema/-/blob/147676fbe48d4917fb26a14f0044912172542574/app_info.schema.json"
    "plcnextapp": {
        ...
    }
}
```

The schema can also be referenced as a local file:

```json
{
    "$schema": "./app_info.schema.json"
    "plcnextapp": {
        ...
    }
}
```

Additionally, the schema file can be set up to be used for any `app_info.json` in Visual Studio Code as specified in the [documentation](https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings).

### Command Line Tools

There are command line tools, that implement the validation against JSON schemas and come in handy when used in a CICD pipeline or as part of a local build process of the PLCnext Control App.

### Web Tools

To quickly verify the validity without any installed tools, you may use an [online JSON schema validator](https://www.jsonschemavalidator.net/), that supports draft `2020-12`.



