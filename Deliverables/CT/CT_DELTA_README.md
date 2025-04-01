## Overview

The **CT_DELTA_\<first version\>_\<second version\>.csv** files in this folder show the changes made to the entity, attribute and relationship information represented on the **DDF Entities&Attributes** sheet of the USDM_CT.xlsx terminology file for the second version of USDM specified in the file name as compared to the first version.

Each row in the CSV file represents a change to the characteristic of either a class or an attribute/relationship of a class.

The **Class Status** column (Column B) indicates whether the class named in the **Class Name** column (Column A) has been added, deleted or modified.

The **Attribute/Relationship Status** column (Column E) indicates whether the attribute or relationship named in the **Attribute/Relationship Name** column (Column D) has been added, deleted or modified.

- When a class has been added, all characteristics of the new class and its attributes/relationships are shown on separate rows, with the new characteristic value shown in the **New Value** column.
- When a class has been deleted, all characteristics of the old class and its attributes/relationships are shown on separate rows, with the previous characteristic shown in the **Old Value** column.
- When a class, attribute or relationship has been modified, all characteristics of the modified class, attribute or relationship are shown on separate rows, with the previous and new values or the characteristic shown in the **Old Value** and **New Value** columns respectively.

## Characteristics

Unless specified in the table below, the values used in the **Class Characteristic** column (Column C) and the **Attribute/Relationship Characteristic** column (Column F) correspond with the column headings on the **DDF Entities&Attributes** sheet of the USDM_CT.xlsx file.

| Column                                           | Value               | Description                                                                                                                                                                                                                                                                          |
| ------------------------------------------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Class Characteristic** *(Column C)*                  | Super Classes        | The name(s) of any general, or "super", class(es) from which this class inherits attributes or relationships. This is derived as a unique list of the values specified in the "Inherited From" column of the USDM_CT spreadsheet for any of the class's attributes or relationships. |
|                                                  | Sub Classes          | The name(s) of class(es) that inherited attributes or relationships from this class. This is derived as a unique list of the classes that include this class as a "super" class.                                                                                                     |
|                                                  | Attributes/Relationships          | The attributes and relationships defined for the class. This is the value shown on all rows representing changes to individual attributes or relationships.                                                                                                                          |
| **Attribute/Relationship Characteristic** *(Column F)* | Model Representation | Indicates whether the class property is represented as an attribute or a relationship. This is derived from the value from the "Role" column - the model representation is set as "Attribute" if the role is "Complex Datatype Relationship", otherwise it is the same as the role.  |
|                                                  | Codelist Reference   | The codelist reference extracted from within the parentheses of any value of the "Has Value List" column that is in the form "Y (\<codelist reference\>)".                                                                                                                             |