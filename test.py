import json
import pytest
from jsonschema import ValidationError, validate


@pytest.fixture
def schema():
    with open("./app_info.schema.json") as file:
        return json.load(file)

@pytest.fixture
def minimal_plcnextapp():
    return {
        "plcnextapp": {
            "name": "Test App",
            "identifier": "00000000000000",
            "version": "1.0.0",
            "target": "AXC F 2152",
            "minfirmware_version": "2024.0.0"
        }
    }

@pytest.fixture
def complete_plcnextapp(minimal_plcnextapp):
    optional_props = {
        "manufacturer": "Phoenix Contact GmbH & Co. KG",
        "licensetype": "Free",
        "linkToAppPage": "www.plcnextstore.com",
        "additionalInfo": [
            { 
                "key": "page_url", 
                "value": "Company Web Page", 
                "url": "https://plcnextstore.com",
                "type": "ExternalLink"
            }
        ],
    }
    return {
        "plcnextapp": { **minimal_plcnextapp["plcnextapp"], **optional_props }
    }

@pytest.fixture
def engineerapp(complete_plcnextapp):
    return {
        **complete_plcnextapp,
        "engineerapp": {
            "folder": "/path/to/PCWE"
        }
    }

@pytest.fixture
def plcnextextensions(complete_plcnextapp):
    return {
        **complete_plcnextapp,
        "plcnextextensions": [
            { "acfconfigpath": "/path/to/my.acf.config"}
        ]
    }

@pytest.fixture
def linuxdaemons(complete_plcnextapp):
    return {
        **complete_plcnextapp,
        "linuxdaemons": [
            { 
                "path": "/path/to/daemon",
                "cmdargs": "--arg test --next-arg next-test",
                "starttime": "99",
                "initScriptTemplate": "/path/to/init.sh"
            }
        ]
    }

@pytest.fixture
def sharedlibs(complete_plcnextapp):
    return {
        **complete_plcnextapp,
        "sharedlibs": [
            { "libpath": "/path/to/lib.so"}
        ]
    }

@pytest.fixture
def ocicontainer(complete_plcnextapp):
    return {
        **complete_plcnextapp,
        "ocicontainer": {
            "quadletFiles": [
                { "path": "/path/to/file", "type": "Main" }
            ],
            "environmentVarialbes": [
                { "name": "TEST_VAR", "value": "test" }
            ],
            "images": [
                { 
                    "name": "Test Image",
                    "id": "57f067446d29f661ee55e675aff86527f4817933f10592f6f3d34870b99fed04",
                    "path": "/path/to/image.tar.gz"
                }
            ]
        }
    }

@pytest.fixture
def datastorage(complete_plcnextapp):
    return {
        **complete_plcnextapp,
        "datastorage": {
            "persistentdata": True,
            "temporarydata": False,
            "directoriesToCreate": {
                "temporary": [ { "path": "/path/to/dir" } ],
                "persistent": [ { "path": "/path/to/dir" } ]
            }
        }
    }

@pytest.fixture
def plcnextservices(complete_plcnextapp):
    return {
        **complete_plcnextapp,
        "plcnextservices": [
            { "service": "WBM", "action": "MUST_HAVE" }
        ]
    }

@pytest.fixture
def updateconfigs(complete_plcnextapp):
    return {
        **complete_plcnextapp,
        "updateconfigs": {
            "autoupdate_enabled": False,
            "keep_persistentdata": True,
            "keep_temporarydata": True,
            "post_updatescript": "/path/to/script.sh"
        }
    }

# [[ plcnextapp ]]

def test_minimal_plcnextapp_is_valid(schema, minimal_plcnextapp):
    validate(instance=minimal_plcnextapp, schema=schema)

def test_plcnextapp_missing_name(schema, minimal_plcnextapp):
    del minimal_plcnextapp["plcnextapp"]["name"]
    with pytest.raises(ValidationError):
        validate(instance=minimal_plcnextapp, schema=schema)

@pytest.mark.parametrize("minfirmware_version", ["24.0", "24", "abc", "25.0.0.0"])
def test_plcnextapp_invalid_firmware(schema, minimal_plcnextapp, minfirmware_version):
    minimal_plcnextapp["plcnextapp"]["minfirmware_version"] = minfirmware_version
    with pytest.raises(ValidationError):
        validate(instance=minimal_plcnextapp, schema=schema)

@pytest.mark.parametrize("target", [
    "AXC F 2152,",
    "AXC F 2152 ", 
    "AXC F 2152, ", 
    "AXC F 2152, AXC F 3152", 
    "AXC F 2152 ,AXC F 3152", 
    "AXC F 2152 , AXC F 3152", 
    "", 
    None])
def test_plcnextapp_invalid_target(schema, minimal_plcnextapp, target):
    minimal_plcnextapp["plcnextapp"]["target"] = target
    with pytest.raises(ValidationError):
        validate(instance=minimal_plcnextapp, schema=schema)

@pytest.mark.parametrize("identifier", ["1234", 00000000000000, ""])
def test_plcnextapp_invalid_identifier(schema, minimal_plcnextapp, identifier):
    minimal_plcnextapp["plcnextapp"]["identifier"] = identifier
    with pytest.raises(ValidationError):
        validate(instance=minimal_plcnextapp, schema=schema)

def test_complete_plcnextapp_is_valid(schema, complete_plcnextapp):
    validate(instance=complete_plcnextapp, schema=schema)

@pytest.mark.parametrize("_type", ["ExternalLink", "LocalLink", "PortLink"])
def test_plcnextapp_additionalInfo_item_missing_url(schema, complete_plcnextapp, _type):
    # For InfoText a missing url should be fine
    complete_plcnextapp["plcnextapp"]["additionalInfo"][0]["type"] = "InfoText"
    del complete_plcnextapp["plcnextapp"]["additionalInfo"][0]["url"]
    validate(instance=complete_plcnextapp, schema=schema)
    # Restore url
    complete_plcnextapp["plcnextapp"]["additionalInfo"][0]["url"] = "http://plcnextstore.com"

    complete_plcnextapp["plcnextapp"]["additionalInfo"][0]["type"] = _type
    del complete_plcnextapp["plcnextapp"]["additionalInfo"][0]["url"]
    with pytest.raises(ValidationError):
        validate(instance=complete_plcnextapp, schema=schema)

def test_plcnextapp_additionalInfo_is_empty(schema, complete_plcnextapp):
    complete_plcnextapp["plcnextapp"]["additionalInfo"] = []
    with pytest.raises(ValidationError):
        validate(instance=complete_plcnextapp, schema=schema)

# [[ plcnextextensions ]]

@pytest.mark.parametrize("acfconfigpath", ["/my/my.config", "my.acf", "", ".my.acf.config"])
def test_plcnextextensions_items_invalid_acfconfigpath(schema, plcnextextensions, acfconfigpath):
    plcnextextensions["plcnextextensions"][0] = acfconfigpath
    with pytest.raises(ValidationError):
        validate(instance=minimal_plcnextapp, schema=schema)

# [[ linuxdaemons ]]

def test_linuxdaemons_is_valid(schema, linuxdaemons):
    validate(instance=linuxdaemons, schema=schema)

def test_linuxdaemons_items_missing_initScriptTemplate_is_valid(schema, linuxdaemons):
    del linuxdaemons["linuxdaemons"][0]["initScriptTemplate"]
    validate(instance=linuxdaemons, schema=schema)

@pytest.mark.parametrize("starttime", [99, "abc", ""])
def test_linuxdaemons_items_invalid_starttime(schema, linuxdaemons, starttime):
    linuxdaemons["linuxdaemons"][0]["starttime"] = starttime
    with pytest.raises(ValidationError):
        validate(instance=linuxdaemons, schema=schema)

# [[ sharedlibs ]]

def test_sharedlibs_is_valid(schema, sharedlibs):
    validate(instance=sharedlibs, schema=schema)

@pytest.mark.parametrize("libpath", ["", "/path/lib..so", "/path/lib.a", "lib"])
def test_sharedlibs_items_invalid_libpath(schema, sharedlibs, libpath):
    sharedlibs["sharedlibs"][0]["libpath"] = libpath
    with pytest.raises(ValidationError):
        validate(instance=linuxdaemons, schema=schema)

def test_sharedlibs_items_is_empty(schema, sharedlibs):
    sharedlibs["sharedlibs"] = []
    with pytest.raises(ValidationError):
        validate(instance=linuxdaemons, schema=schema)

# [[ ocicontainer ]]

def test_ocicontainer_is_valid(schema, ocicontainer):
    validate(instance=ocicontainer, schema=schema)

def test_ocicontainer_quadletfiles_items_invalid_type(schema, ocicontainer):
    ocicontainer["ocicontainer"]["quadletFiles"][0]["type"] = "Wrong"
    with pytest.raises(ValidationError):
        validate(instance=ocicontainer, schema=schema)

def test_ocicontainer_quadletfiles_items_missing_type(schema, ocicontainer):
    del ocicontainer["ocicontainer"]["quadletFiles"][0]["type"]
    validate(instance=ocicontainer, schema=schema)

@pytest.mark.parametrize("id", [
    "", 
    "57f067446d29f661ee55e675aff86527f4817933f10592f6f3d34870b99fed0", 
    "57g067446d29f661ee55e675aff86527f4817933f10592f6f3d34870b99fed04", 
    "57g067446d29f661ee55e675aff86527f4817933f10592f6f3d34870b99fed044"
])
def test_ocicontainer_images_items_invalid_id(schema, ocicontainer, id):
    ocicontainer["ocicontainer"]["images"][0]["id"] = id
    with pytest.raises(ValidationError):
        validate(instance=ocicontainer, schema=schema)

# [[ datastorage ]]

def test_datastorage_is_valid(schema, datastorage):
    validate(instance=datastorage, schema=schema)

def test_datastorage_is_empty(schema, datastorage):
    del datastorage["datastorage"]["persistentdata"]
    del datastorage["datastorage"]["temporarydata"]
    with pytest.raises(ValidationError):
        validate(instance=datastorage, schema=schema)

# [[ plcnextservices ]]

def test_plcnextservices_is_valid(schema, plcnextservices):
    validate(instance=plcnextservices, schema=schema)

def test_plcnextservices_items_invalid_service(schema, plcnextservices):
    plcnextservices["plcnextservices"][0]["service"] = "WRONG"
    with pytest.raises(ValidationError):
        validate(instance=ocicontainer, schema=schema)

def test_plcnextservices_items_invalid_action(schema, plcnextservices):
    plcnextservices["plcnextservices"][0]["action"] = "WRONG"
    with pytest.raises(ValidationError):
        validate(instance=ocicontainer, schema=schema)

def test_plcnextservices_items_missing_action(schema, plcnextservices):
    del plcnextservices["plcnextservices"][0]["action"]
    with pytest.raises(ValidationError):
        validate(instance=ocicontainer, schema=schema)

# [[ updateconfigs ]]

def test_updateconfigs_is_valid(schema, updateconfigs):
    validate(instance=updateconfigs, schema=schema)

def test_updateconfigs_missing_autoupdate(schema, updateconfigs):
    del updateconfigs["updateconfigs"]["autoupdate_enabled"]
    with pytest.raises(ValidationError):
        validate(instance=updateconfigs, schema=schema)

# [[ defs ]]

@pytest.mark.parametrize("path", ["//path", "/ path", "", "path//"])
def test_invalid_path_def(schema, engineerapp, path):
    engineerapp["engineerapp"]["folder"] = path
    with pytest.raises(ValidationError):
        validate(instance=minimal_plcnextapp, schema=schema)

