## Overview

The **API_DELTA_\<first version\>_\<second version\>.csv** files in this folder show the changes made to the information represented in the USDM_API.json API specification for the second version of USDM specified in the file name as compared to the first version.

Each row in the CSV file represents a change to the characteristic of either a class or an attribute/relationship of a class.

The **Class Status** column (Column B) indicates whether the class named in the **Class Name** column (Column A) has been added, deleted or modified.

The **Attribute/Relationship Status** column (Column E) indicates whether the attribute or relationship named in the **Attribute/Relationship Name** column (Column D) has been added, deleted or modified.

- When a class has been added, all characteristics of the new class and its attributes/relationships are shown on separate rows, with the new characteristic value shown in the **New Value** column.
- When a class has been deleted, all characteristics of the old class and its attributes/relationships are shown on separate rows, with the previous characteristic shown in the **Old Value** column.
- When a class, attribute or relationship has been modified, all characteristics of the modified class, attribute or relationship are shown on separate rows, with the previous and new values or the characteristic shown in the **Old Value** and **New Value** columns respectively.

## Characteristics

Descriptions of the class and attribute/relationship characteristics are shown below.

| Column                                           | Value       | Description                                                                                                                                                           |
| ------------------------------------------------ | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Class Characteristic** *(Column C)*                  | Attributes/Relationships  | The attributes and relationships defined for the class. This is the value shown on all rows representing changes to individual attributes or relationships.           |
| **Attribute/Relationship Characteristic** *(Column F)* | Data Types       | The data type(s) specified for the attribute/relationship.May include primitive data types such as "string", "integer", etc. or references to other USDM class names. |
|                                                  | Cardinality | The cardinality specified for the attribute.                                                                                                                          |