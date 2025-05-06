# CORE Test Data Template

The `CORE Test Data Template.xlsx` file provides a template for the creation of test data in Excel format for use in the [CORE Rule Editor](https://rule-editor.cdisc.org/) when testing rules that check USDM data that has been converted to tabular format by the CORE USDM data service. The template file is generated programmatically from the same combination of the following USDM artefacts that is used to generate USDM deliverables such as the `Deliverables/UML/dataStructure.yml` and `Deliverables/UML/dataDictionary.MD` files:
- The UML model definition (exported in XMI format)
- The API specification
- The CT definitions

The template file contains:
- A `Datasets` sheet, which acts as an index and contains one row for each non-abstract USDM class.
- One sheet for each non-abstract USDM class, each of which contains columns corresponding to the class-specific columns in the tabular representation of USDM data that would be created by the CORE USDM data service.  The columns include:
    - Four "system" columns that indicate the positioning of the represented data records within the original JSON hierarchy:
        - `parent_entity`: The name of the parent class
        - `parent_id`: The `id` value for the instance of the parent class
        - `parent_rel`: The name of the attribute or relationship in the parent class that contains the represented data
        - `rel_type`: An indication of whether the represented data is specified as a "definition" or a "reference":
            - "definition": The represented data is present in the original JSON as a class instance (i.e., including specifications of each attribute value)
            - "reference": The represented data is referenced by `id` value in the original JSON.
    - One column for each of the class attributes (apart from extension attributes), which may contain one of the following:
        - For attributes with a primitive data type (e.g. String, Float, etc.) that allow a maximum of one value, the value of the attribute.
        - For attributes that have a complex data type or allow more than one value, a boolean indication of whether the attribute contains any value(s).
    - One column for each of the attributes of any child class that is referenced as a complex data type when no more than one value is allowed. The name of each of these columns indicates the data path using dot notation (e.g., `type.code` indicates the `code` attribute of the `Code` class that represents the value of the `type` attribute), and these columns are populated in the same way as described in the previous bullet. Columns for multiple levels of flattened hierarchical data may be included as long as the number of allowed values does not exceed 1 (e.g., `plannedAge.minValue.unit.standardCode.decode` might contain the decode for the standard code of the unit for the minimum value of the planned age range).

## Usage

Only the sheets referenced by the tested rule need to be included and populated, so the following process can be followed:

1. Make a copy of the template file and rename it (usually according to the tested rule identifier).
2. Delete any rows representing unneeded classes from the `Dataset` sheet.
3. Delete any sheets representing unneeded classes.
4. Resolve any duplicate column names (highlighted in red) by deleting one or both of the duplicate columns. These are created when an attribute allows data values to be represented using different classes as complex data types (e.g. `Quantity` or `Range`).
      1. If only one type of child value is required, delete all columns for the unneeded child class attributes.
      2. If both types of child value are required, delete the duplicate columns for the second class and enter all values for the named attribute in the same column. If preferred, the label and cardinality for the remaining columns can be updated to indicate that they contain values for both child data types.
5. Enter test data on the remaining sheets, with each row representing an instance of the class.
6. Save the file.
7. Upload the test file by clicking the `TEST DATASETS FILE...` button in the `Load Test Datasets` section of the `TEST` tab in the CORE Rule Editor.