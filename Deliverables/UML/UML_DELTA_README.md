## Overview

The **UML_DELTA_\<first version\>_\<second version\>.csv** files in this folder show the changes made to the information represented in the UML model for the second version of USDM specified in the file name as compared to the first version.

Each row in the CSV file represents a change to the characteristic of either a class or an attribute/relationship of a class.

The **Class Status** column (Column B) indicates whether the class named in the **Class Name** column (Column A) has been added, deleted or modified.

The **Attribute/Relationship Status** column (Column E) indicates whether the attribute or relationship named in the **Attribute/Relationship Name** column (Column D) has been added, deleted or modified.

- When a class has been added, all characteristics of the new class and its attributes/relationships are shown on separate rows, with the new characteristic value shown in the **New Value** column.
- When a class has been deleted, all characteristics of the old class and its attributes/relationships are shown on separate rows, with the previous characteristic shown in the **Old Value** column.
- When a class, attribute or relationship has been modified, all characteristics of the modified class, attribute or relationship are shown on separate rows, with the previous and new values or the characteristic shown in the **Old Value** and **New Value** columns respectively.

## Characteristics

Descriptions of the class and attribute/relationship characteristics are shown below.

| Column                                           | Value               | Description                                                                                                                                                                                                                                                                         |
| ------------------------------------------------ | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Class Characteristic** *(Column C)*                  | Abstract          | A true/false indication of whether the class is an abstract class as specified by the Abstract checkbox property of the UML class. Instances containing data are never created for abstract classes.                                                                                |
|                                                  | Super Classes        | The name(s) of any general, or "super", class(es) from which this class inherits attributes or relationships, as indicated by inheritance relationships specified in the UML model.                                                                                                 |
|                                                  | Sub Classes          | The name(s) of class(es) that inherited attributes or relationships from this class. This is derived as a unique list of the classes that include this class as a "super" class.                                                                                                    |
|                                                  | Attributes/Relationships          | The attributes and relationships defined for the class. This is the value shown on all rows representing changes to individual attributes or relationships.                                                                                                                         |
| **Attribute/Relationship Characteristic** *(Column F)* | Data Types               | The data type(s) specified for the attribute/relationship, as indicated either by the data type specified for UML attributes or the target class for UML relationships. May include primitive data types such as "String", "Integer", etc. or references to other USDM class names. |
|                                                  | Model Representation | Indicates whether the class property is represented as an attribute or a relationship in the UML model.                                                                                                                                                                             |
|                                                  | Inherited From       | Identifies the general class from which the attribute or relationship is inherited, as indicated by inheritance relationships in the UML model.                                                                                                                                     |
|                                                  | Cardinality         | The cardinality specified for the UML attribute or the target cardinality for the UML relationship.                                                                                                                                                                                 |