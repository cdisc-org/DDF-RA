|Class Name|Attribute Name|Data Type|NCI C-Code|Cardinality|Preferred Term|Definition|Codelist Ref|Inherited From|
|---|---|---|---|---|---|---|---|---|
|Abbreviation|||C42610||Abbreviation|A set of letters that are drawn from a word or from a sequence of words and that are used for brevity in place of the full word or phrase. (CDISC Glossary)|||
||id|String||1|||||
||abbreviatedText|String|C215487|1|Text Abbreviation Value|The literal value of an instance of unstructured text that is used as the abbreviation.
|||
||expandedText|String|C215569|1|Abbreviation Long Name|The full literal representation of the abbreviation.|||
||notes|CommentAnnotation|C215570|0..*|Abbreviation Notes|A brief written record relevant to the abbreviation.|||
|Activity|||C71473||Study Activity|An action, undertaking, or event, which is anticipated to be performed or observed, or was performed or observed, according to the study protocol during the execution of the study.|||
||id|String||1|||||
||name|String|C188842|1|Study Activity Name|The literal identifier (i.e., distinctive designation) of the study activity.|||
||label|String|C207458|0..1|Study Activity Label|The short descriptive designation for the study activity.|||
||description|String|C70960|0..1|Study Activity Description|A narrative representation of the study activity.|||
||notes|CommentAnnotation|C215519|0..*|Activity Notes|A brief written record relevant to the activity.|||
||definedProcedures|Procedure||0..*||A USDM relationship between the Activity and Procedure classes which identifies the set of defined procedures associated with the activity.|||
||biomedicalConcepts|BiomedicalConcept||0..*||A USDM relationship between the Activity and BiomedicalConcept classes which identifies the set of biomedical concepts associated with the activity.|||
||next|Activity||0..1||A USDM relationship within the Activity class which identifies the activity that follows the current activity in the display order.|||
||timeline|ScheduleTimeline||0..1||A USDM relationship between the Activity and ScheduleTimeline classes which provides the details associated with an instance of the scheduled timeline related to the activity.|||
||children|Activity||0..*||A USDM relationship within the Activity class which identifies the set of child activities associated with an activity.|||
||previous|Activity||0..1||A USDM relationship within the Activity class which identifies the activity that precedes the current activity in the display order.|||
||bcSurrogates|BiomedicalConceptSurrogate||0..*||A USDM relationship between the Activity and BiomedicalConceptSurrogate classes which identifies the set of biomedical concept surrogates associated with the activity.|||
||bcCategories|BiomedicalConceptCategory||0..*||A USDM relationship between the Activity and BiomedicalConceptCategory classes which identifies the set of biomedical concept categories associated with the activity.|||
|Address|||C25407||Address|A standardized representation of the location of a person, business, building, or organization. (NCI)|||
||id|String||1|||||
||text|String|C201311|0..1|Address Full Text|A standardized representation of the complete set of components denoting the physical address of the person, business, building, or organization.|||
||lines|String|C25690|0..*|Address Line|The street name and number, building number, apartment or unit number, or post office box number where an entity is physically located.|||
||district|String|C176229|0..1|District|An administrative or territorial division of a city, town, county, parish, state, country, or other locality based on a shared characteristic.|||
||city|String|C25160|0..1|City|A relatively large and/or densely populated area of human habitation with administrative or legal status that may be specified as a component of a postal address.|||
||postalCode|String|C25621|0..1|Postal Code|An alphanumeric code assigned to a mail delivery area.|||
||state|String|C87194|0..1|State|A sub-division of a country that forms part of a federal union. States are usually, but not always, more autonomous than provinces and may have different laws from the central government.|||
||country|Code|C25464|0..1|Country|A sovereign nation occupying a distinct territory and ruled by an autonomous government.|Point out to ISO 3166-1 Alpha-3 Country code||
|AdministrableProduct|||C215492||Administrable Product|Any study product that is formulated and presented in the form that is suitable for administration to a study participant.|||
||id|String||1|||||
||name|String|C215573|1|Administrable Product Definition Name|The literal identifier (i.e., distinctive designation) of the administrable product.|||
||label|String|C215575|0..1|Administrable Product Definition Label|The short descriptive designation for the administrable product.|||
||description|String|C215574|0..1|Administrable Product Definition Description|A narrative representation of the administrable product.|||
||administrableDoseForm|AliasCode|C215576|1|Administrable Product Dose Form|The physical form in which formulated ingredient(s) are presented in the administrable product.|SDTM Terminology Codelist C66726||
||sourcing|Code|C215578|0..1|Administrable Product Sourcing|An indication as to whether the administrable product is obtained from a local or central source.|CNEW - Product Sourcing Value Set||
||productDesignation|Code|C215579|1|Administrable Product Product Designation|An indication as to whether the administrable product is an investigational medicinal product or an auxiliary medicinal product.|C207418||
||pharmacologicClass|Code|C215577|0..1|Administrable Product Pharmacologic Class|The pharmacological class of the administrable product.|Points to external codelists such as UNII, MED-RT||
||notes|CommentAnnotation|C215580|0..*|Administrable Product Notes|A brief written record relevant to the administrable product.|||
||identifiers|AdministrableProductIdentifier||0..*||A USDM relationship between the AdministrableProduct and AdministrableProductIdentifier classes which provides the set of identifiers related to the administrable product.|||
||properties|AdministrableProductProperty||0..*||A USDM relationship between the AdministrableProduct and AdministrableProductProperty classes which provides the set of properties related to the administrable product.|||
||ingredients|Ingredient||0..*||A USDM relationship between the AdministrableProduct and Ingredient classes which provides the set of ingredients related to the administrable product.|||
|AdministrableProductIdentifier|||C215493||Administrable Product Identifier|A sequence of characters used to identify, name, or characterize the administrable product.|||
||id|String||1|||||
||text|String|C215581|1|Administrable Product Identifier Text|An instance of structured text that represents the administrable product.||Identifier|
||scope|Organization||1||A USDM relationship between the AdministrableProductIdentifier and Organization class which provides the details associated with which provides the details associated with each organization that has assigned the administrable product identifier.||Identifier|
|AdministrableProductProperty|||C215494||Administrable Product Property|A characteristic from a set of characteristics used to define an administrable product.|||
||id|String||1|||||
||name|String|C215582|1|Administrable Product Property Name|The literal identifier (i.e., distinctive designation) of the administrable product property.|||
||type|Code|C215585|1|Administrable Product Property Type|A characterization or classification of the administrable product property.|CNEW Administrable Product Property Type||
||text|String|C215583|1|Administrable Product Property Text|An instance of structured text that represents the administrable product property.|||
||quantity|Quantity|C215584|0..1|Administrable Product Property Quantity Value|The numeric value associated with an administrable product property.|||
|Administration|||C25409||Administration|The act of dispensing, applying, or tendering a product, agent, or therapy.|||
||id|String||1|||||
||name|String|C207465|1|Administration Name|The literal identifier (i.e., distinctive designation) for the administration of a product, agent, or therapy.|||
||label|String|C207464|0..1|Administration Label|The short descriptive designation for the administration of a product, agent, or therapy.|||
||description|String|C207463|0..1|Administration Description|A narrative representation for the administration of a product, agent, or therapy.|||
||dose|Quantity|C167190|0..1|Administration Dose|The value representing the amount of an agent given to an individual at one time.|||
||frequency|AliasCode|C89081|0..1|Dosing Frequency|The number of doses administered per a specific interval.|SDTM Terminology Codelist C71113||
||route|AliasCode|C38114|0..1|Route of Administration|The pathway by which a substance is administered in order to reach the site of action in the body.|SDTM Terminology Codelist C66729||
||notes|CommentAnnotation|C215544|0..*|Administration Notes|A brief written record relevant to the administration of the product, agent, or therapy.|||
||administrableProduct|AdministrableProduct||0..1||A USDM relationship between the Administration and AdministrableProductDefinition classes which identifies the administrable product associated with the administration of the product, agent, or therapy.|||
||duration|AdministrationDuration||1||A USDM relationship between the Administration and AdministrationDuration classes which provides the duration of an instance of product, agent, or therapy administration.|||
||medicalDevice|MedicalDevice||0..1||A USDM relationship between the Administration and MedicalDevice classes which identifies the medical device associated with an instance of product, agent, or therapy administration.|||
|AdministrationDuration|||C69282||Administration Duration|The amount of time elapsed during the administration of an agent.|||
||id|String||1|||||
||description|String|C207459|0..1|Administration Duration Description|A narrative representation of the agent administration duration.|||
||quantity|Quantity|C207460|0..1|Administration Duration Quantity Value|The value representing the amount of time over which the administration of an agent occurs.|||
||durationWillVary|Boolean|C207461|1|Administration Duration Will Vary Indicator|An indication as to whether the agent administration duration is planned to vary within and/or across subjects.|||
||reasonDurationWillVary|String|C207462|0..1|Administration Duration Reason Duration Will Vary|The explanation for why the agent administration duration will vary within and/or across subjects.|||
|AliasCode|||C201344||Alias Code|An alternative symbol or combination of symbols which is assigned to the members of a collection.|||
||id|String||1|||||
||standardCode|Code|C215528|1|Standard Code|A combination of symbols that is used to represent the standard code.|||
||standardCodeAliases|Code|C215529|0..*|Standard Code Aliases|Alternative combinations of symbols used to represent aliases or alternatives to the standard code.|||
|AnalysisPopulation|||C188814||Analysis Population|A target study population on which an analysis is performed. These may be represented by the entire study population, a subgroup defined by a particular characteristic measured at baseline, or a principal stratum defined by the occurrence (or non-occurrence, depending on context) of a specific intercurrent event. (ICH E9 R1 Addendum)|||
||id|String||1|||||
||text|String|C207468|1|Analysis Population Text|An instance of unstructured text that represents the analysis population.|||
||name|String|C207467|1|Analysis Population Name|The literal identifier (i.e., distinctive designation) of the analysis population.|||
||label|String|C207466|0..1|Analysis Population Label|The short descriptive designation for the analysis population.|||
||description|String|C188854|0..1|Analysis Population Description|A narrative representation of the analysis population.|||
||notes|CommentAnnotation|C215525|0..*|Analysis Population Notes|A brief written record relevant to the analysis population.|||
||subsetOf|PopulationDefinition||0..*||A USDM relationship between the AnalysisPopulation and PopulationDefinition classes which identifies the population definition of which the analysis population is a subset.|||
|AssignedPerson|||C215496||Assigned Person|An individual person who is allotted or appointed to a particular role, function, or other entity.|||
||id|String||1|||||
||name|String|C215596|1|Assigned Person Name|The literal identifier (i.e., distinctive designation) of the assigned person.|||
||label|String|C215598|0..1|Assigned Person Label|The short descriptive designation for the assigned person.|||
||description|String|C215597|0..1|Assigned Person Description|A narrative representation of the assigned person.|||
||personName|HumanName||1|||||
||jobTitle|String|C215599|1|Assigned Person Job Title|An identifying designation related to the assigned person's occupation.|||
||organization|Organization||0..1||A USDM relationship between the AssignedPerson and Organization classes that identifies that organization to which the assigned person belongs.|||
|BiomedicalConcept|||C201345||Biomedical Concept|A unit of biomedical knowledge created from a unique combination of characteristics that include implementation details like variables and terminologies, used as building blocks for standardized, hierarchically structured clinical research information.|||
||id|String||1|||||
||name|String|C201312|1|Biomedical Concept Name|The literal identifier (i.e., distinctive designation) of the biomedical concept.|||
||label|String|C207470|0..1|Biomedical Concept Label|The short descriptive designation for the biomedical concept.|||
||synonyms|String|C201314|0..*|Biomedical Concept Synonym|A word or an expression that serves as a figurative, symbolic, or exact substitute for a biomedical concept, and which has the same meaning.|||
||reference|String|C201313|1|Biomedical Concept Reference|A citation to an authoritative source for a biomedical concept.|||
||code|AliasCode|C207469|1|Biomedical Concept Concept Code|A concept unique identifier assigned to a biomedical concept that points to the meaning of that biomedical concept.|||
||notes|CommentAnnotation|C215530|0..*|Biomedical Concept Notes|A brief written record relevant to the biomedical concept.|||
||properties|BiomedicalConceptProperty||0..*||A USDM relationship between the BiomedicalConcept and BiomedicalConceptProperty classes which identifies the set of properties associated with the biomedical concept.|||
|BiomedicalConceptCategory|||C201346||Biomedical Concept Category|A grouping of biomedical concepts based on some commonality or by user defined characteristics.|||
||id|String||1|||||
||name|String|C201317|1|Biomedical Concept Category Name|The literal identifier (i.e., distinctive designation) of the biomedical concept category.|||
||label|String|C207471|0..1|Biomedical Concept Category Label|The short descriptive designation for the biomedical concept category.|||
||description|String|C201316|0..1|Biomedical Concept Category Description|A narrative representation of the biomedical concept category.|||
||code|AliasCode|C201315|0..1|Biomedical Concept Category Code|A symbol or combination of symbols which is assigned to the biomedical concept category.|||
||notes|CommentAnnotation|C215533|0..*|Biomedical Concept Category Notes|A brief written record relevant to the biomedical concept category.|||
||members|BiomedicalConcept||0..*||A USDM relationship between the BiomedicalConceptCategory and BiomedicalConcept classes which identifies the set of biomedical concept members associated with the biomedical concept category.|||
||children|BiomedicalConceptCategory||0..*||A USDM relationship within the BiomedicalConceptCategory class which identifies the set of child categories of a biomedical concept.|||
|BiomedicalConceptProperty|||C202493||Biomedical Concept Property|A characteristic from a set of characteristics used to define a biomedical concept.|||
||id|String||1|||||
||name|String|C202494|1|Biomedical Concept Property Name|The literal identifier (i.e., distinctive designation) of the biomedical concept property.|||
||label|String|C207472|0..1|Biomedical Concept Property Label|The short descriptive designation for the biomedical concept property.|||
||isRequired|Boolean|C202495|1|Biomedical Concept Property Required Indicator|An indication as to whether the biomedical concept property is required.|||
||isEnabled|Boolean|C202496|1|Biomedical Concept Property Enabled Indicator|An indication as to whether the biomedical concept property is activated for use within a given usage context for a biomedical concept.|||
||datatype|String|C201319|1|Biomedical Concept Property Response Data Type|The structural format of the biomedical concept property response value. The datatype is carried in the attribute and influences the set of allowable values the attribute may assume. (After HL7)|||
||code|AliasCode|C201318|1|Biomedical Concept Property Concept Code|A concept unique identifier assigned to a biomedical concept property that points to the meaning of that biomedical concept property.|||
||notes|CommentAnnotation|C215531|0..*|Biomedical Concept Property Notes|A brief written record relevant to the biomedical concept property.|||
||responseCodes|ResponseCode||0..*||A USDM relationship between the BiomedicalConceptProperty and ResponseCode classes which identifies the set of response codes associated with the biomedical concept property.|||
|BiomedicalConceptSurrogate|||C207590||Biomedical Concept Surrogate|A concept that substitutes for a standard biomedical concept from the designated source.|||
||id|String||1|||||
||name|String|C207474|1|Biomedical Concept Surrogate Name|The literal identifier (i.e., distinctive designation) of the biomedical concept surrogate.|||
||label|String|C207473|0..1|Biomedical Concept Surrogate Label|The short descriptive designation for the biomedical concept surrogate.|||
||description|String|C201320|0..1|Biomedical Concept Surrogate Description|A narrative representation of the biomedical concept surrogate.|||
||reference|String|C201321|0..1|Biomedical Concept Surrogate Reference|A citation to an authoritative source for a biomedical concept surrogate.|||
||notes|CommentAnnotation|C215532|0..*|Biomedical Concept Surrogate Notes|A brief written record relevant to the biomedical concept surrogate.|||
|BiospecimenRetention|||C215505||Biospecimen Retention|The continued possession, cataloging, and storage of collected biological specimens beyond their initial use.|||
||id|String||1|||||
||name|String|C215645|1|Biospecimen Retention Name|The literal identifier (i.e., distinctive designation) of the biospecimen retention.|||
||label|String|C215646|0..1|Biospecimen Retention Label|The short descriptive designation for the biospecimen retention.|||
||description|String|C181231|0..1|Biospecimen Retention Description|A narrative representation of the biospecimen retention.|||
||isRetained|Boolean|C164620|1|Biospecimen Retention Indicator|An indication as to whether biospecimens were retained.|||
||includesDNA|Boolean|C127777|0..1|Biospecimen Retention Includes DNA Indicator|An indication as to whether retained biospecimens contain DNA.|||
|Characteristic|||C25447||Characteristic|The distinguishing qualities or prominent aspects of an entity.|||
||id|String||1|||||
||name|String|C207477|1|Characteristic Name|The literal identifier (i.e., distinctive designation) of the characteristic.||SyntaxTemplate|
||label|String|C207476|0..1|Characteristic Label|The short descriptive designation for the characteristic.||SyntaxTemplate|
||description|String|C207475|0..1|Characteristic Description|A narrative representation of the characteristic.||SyntaxTemplate|
||text|String|C207478|1|Characteristic Text|An instance of structured text that represents the characteristic.||SyntaxTemplate|
||notes|CommentAnnotation|C215548|0..*|Characteristic Notes|A brief written record relevant to the characteristic.||SyntaxTemplate|
||dictionary|SyntaxTemplateDictionary||0..1||A USDM relationship between the Characteristic and SyntaxTemplateDictionary classes which provides the set of dictionary entries related to characteristics.||SyntaxTemplate|
|Code|||C25162||Code|A symbol or combination of symbols which is assigned to the members of a collection.|||
||id|String||1|||||
||code|String|C188858|1|Code Value|The literal value of a code.|||
||codeSystem|String|C188859|1|Code System Name|The literal identifier (i.e., distinctive designation) of the system used to assign and/or manage codes.|||
||codeSystemVersion|String|C188868|1|Code System Version|The version of the code system.|||
||decode|String|C188861|1|Decode|Standardized or dictionary-derived human readable text associated with a code.|||
|CommentAnnotation|||C44272||Comment Annotation|An explanatory or critical comment, or other in-context information (e.g., pattern, motif, link), that has been associated with data or other types of information.|||
||id|String||1|||||
||text|String|C215555|1|Comment Annotation Text|An instance of unstructured text that represents the comment annotation.|||
||codes|Code|C215556|0..*|Comment Annotation Code|A symbol or combination of symbols which is assigned to the comment annotation.|||
|Condition|||C25457||Condition|A state of being.|||
||id|String||1|||||
||name|String|C207483|1|Condition Name|The literal identifier (i.e., distinctive designation) of the condition.||SyntaxTemplate|
||label|String|C207482|0..1|Condition Label|The short descriptive designation for the condition.||SyntaxTemplate|
||description|String|C207481|0..1|Condition Description|A narrative representation of the condition.||SyntaxTemplate|
||text|String|C207484|1|Condition Text|An instance of structured text that represents the condition.||SyntaxTemplate|
||notes|CommentAnnotation|C215552|0..*|Condition Notes|A brief written record relevant to the condition.||SyntaxTemplate|
||dictionary|SyntaxTemplateDictionary||0..1||A USDM relationship between the Condition and SyntaxTemplateDictionary classes which provides the set of dictionary entries related to conditions.||SyntaxTemplate|
||context|ScheduledActivityInstance, Activity||0..*||A USDM relationship between the Condition and the ScheduledActivityInstance or Activity classes which identifies the scheduled activity instance or activity to which the condition belongs.|||
||appliesTo|BiomedicalConceptSurrogate, Activity, Procedure, BiomedicalConcept, BiomedicalConceptCategory||0..*||A USDM relationship between the Condition and the Activity, Procedure, BiomedicalConcept, BiomedicalConceptSurrogate, or BiomedicalConceptCategory classes which identifies the procedure, activity, biomedical concept, biomedical concept surrogate, or biomedical concept category that applies to the condition.|||
|ConditionAssignment|||C201335||Condition Assignment|An allotting or appointment to a condition or set of conditions that are to be met in order to make a logical decision.|||
||id|string||1|||||
||condition|String|C47953|1|Logical Condition|An assumption on which rests the validity or effect of something else.|||
||conditionTarget|ScheduledInstance||1||A USDM relationship between the ConditionAssignment and ScheduledInstance classes which identifies the scheduled instance associated with the condition assignment.|||
|DocumentContentReference|||C215499||Document Content Reference|A citation pointing to the location of specific content within a document.|||
||id|String||1|||||
||sectionNumber|String|C215609|1|Document Content Reference Section Number|The numeric identifier of a particular section for the document content reference.|||
||sectionTitle|String|C215610|1|Document Content Reference Section Title|An identifying designation for a particular section for the document content reference.|||
||appliesTo|StudyDefinitionDocument||1||A USDM relationship between the DocumentContentReference and StudyDefinitionDocument classes which identifies the study definition document to which the document content reference applies.|||
|EligibilityCriterion|||C16112||Study Eligibility Criterion|Characteristics which are necessary to allow a subject to participate in a clinical study, as outlined in the study protocol. The concept covers inclusion and exclusion criteria.|||
||id|String||1|||||
||name|String|C207488|1|Study Eligibility Criterion Name|The literal identifier (i.e., distinctive designation) of the study eligibility criterion.|||
||label|String|C207487|0..1|Study Eligibility Criterion Label|The short descriptive designation for the study eligibility criterion.|||
||description|String|C207486|0..1|Study Eligibility Criterion Description|A narrative representation of the study eligibility criterion.|||
||identifier|String|C207489|1|Study Eligibility Criterion Identifier|A sequence of characters used to identify, name, or characterize the inclusion or exclusion criterion.|||
||category|Code|C83016|1|Study Eligibility Criterion Category|A classification of the inclusion exclusion criterion.|SDTM Terminology Codelist C66797||
||notes|CommentAnnotation|C215537|0..*|Eligibility Criterion Notes|A brief written record relevant to the eligibility criterion.|||
||criterionItem|EligibilityCriterionItem||1||A USDM relationship between the EligibilityCriterion and EligibilityCriterionItem classes which identifies the item belonging to the eligibility criterion.|||
||next|EligibilityCriterion||0..1||A USDM relationship within the EligibilityCriterion class which identifies the eligibility criterion that follows the current eligibility criterion in the display order.|||
||previous|EligibilityCriterion||0..1||A USDM relationship within the EligibilityCriterion class which identifies the eligibility criterion that precedes the current eligibility criterion in the display order.|||
|EligibilityCriterionItem|||C215506||Eligibility Criterion Item|An individual item within the container that holds an instance of an eligibility criterion.|||
||id|String||1|||||
||name|String|C215647|1|Eligibility Criterion Item Name|The literal identifier (i.e., distinctive designation) of the eligibility criterion item.||SyntaxTemplate|
||label|String|C215650|0..1|Eligibility Criterion Item Label|The short descriptive designation for the eligibility criterion item.||SyntaxTemplate|
||description|String|C215649|0..1|Eligibility Criterion Item Description|A narrative representation of the eligibility criterion item.||SyntaxTemplate|
||text|String|C215648|1|Eligibility Criterion Item Text|An instance of structured text that represents the eligibility criterion item.||SyntaxTemplate|
||notes|CommentAnnotation|C215651|0..*|Eligibility Criterion Item Notes|A brief written record relevant to the eligibility criterion item.||SyntaxTemplate|
||dictionary|SyntaxTemplateDictionary||0..1||A USDM relationship between the EligibilityCriterionItem and SyntaxTemplateDictionary classes which provides the dictionary entry associated with a eligibility criterion item. ||SyntaxTemplate|
|Encounter|||C215488||Study Encounter|Any physical or virtual contact between two or more parties involved in a study, at which an assessment or activity takes place.|||
||id|String||1|||||
||name|String|C171010|1|Study Encounter Name|The literal identifier (i.e., distinctive designation) for a protocol-defined study encounter.|||
||label|String|C207490|0..1|Study Encounter Label|The short descriptive designation for the study encounter.|||
||description|String|C188836|0..1|Study Encounter Description|A narrative representation of the protocol-defined study encounter.|||
||type|Code|C188839|1|Study Encounter Type|A characterization or classification of the study encounter.|C188728||
||environmentalSettings|Code|C188840|0..*|Environmental Setting|The environment/setting where the event, intervention, or finding occurred.|SDTM Terminology Codelist C127262||
||contactModes|Code|C188841|0..*|Contact Mode|The means by which an interaction occurs between the subject/participant and person or entity (e.g., a device).|SDTM Terminology Codelist C171445||
||notes|CommentAnnotation|C215518|0..*|Encounter Notes|A brief written record relevant to the study encounter.|||
||transitionEndRule|TransitionRule||0..1||A USDM relationship between the Encounter and TransitionRule classes which provides the details associated with a transition rule used to trigger the end of an encounter.|||
||next|Encounter||0..1||A USDM relationship within the Encounter class which identifies the encounter that chronologically follows the current encounter.|||
||transitionStartRule|TransitionRule||0..1||A USDM relationship between the Encounter and TransitionRule classes which provides the details associated with a transition rule used to trigger the start of an encounter.|||
||scheduledAt|Timing||0..1||A USDM relationship between the Encounter and Timing classes which provides information related to the scheduled timing of an encounter.|||
||previous|Encounter||0..1||A USDM relationship within the Encounter class which identifies the encounter that chronologically precedes the current encounter.|||
|Endpoint|||C25212||Study Endpoint|A defined variable intended to reflect an outcome of interest that is statistically analyzed to address a particular research question. NOTE: A precise definition of an endpoint typically specifies the type of assessments made, the timing of those assessments, the assessment tools used, and possibly other details, as applicable, such as how multiple assessments within an individual are to be combined. [After BEST Resource] (CDISC Glossary)|||
||id|String||1|||||
||name|String|C207492|1|Study Endpoint Name|The literal identifier (i.e., distinctive designation) of the study endpoint.||SyntaxTemplate|
||label|String|C207491|0..1|Study Endpoint Label|The short descriptive designation for the study endpoint.||SyntaxTemplate|
||description|String|C188824|0..1|Study Endpoint Description|A narrative representation of the study endpoint.||SyntaxTemplate|
||text|String|C207493|1|Study Endpoint Text|An instance of structured text that represents the study endpoint.||SyntaxTemplate|
||notes|CommentAnnotation|C215514|0..*|Endpoint Notes|A brief written record relevant to the study endpoint.||SyntaxTemplate|
||dictionary|SyntaxTemplateDictionary||0..1||A USDM relationship between the Endpoint and SyntaxTemplateDictionary classes which provides the set of dictionary entries related to study endpoints.||SyntaxTemplate|
||level|Code|C188826|1|Study Endpoint Level|A characterization or classification of the study endpoint that determines its category of importance relative to other study endpoints.|C188726||
||purpose|String|C188825|1|Study Endpoint Purpose Description|The textual representation of the study endpoint purpose.|||
|Estimand|||C188813||Estimand|A precise description of the treatment effect reflecting the clinical question posed by a given clinical trial objective. It summarises at a population level what the outcomes would be in the same patients under different treatment conditions being compared. (ICH E9 R1 Addendum)|||
||id|String||1|||||
||populationSummary|String|C188853|1|Population-Level Summary|A synopsis of the clinical endpoint of interest within the analysis target study population.|||
||name|String|C215522|1|Estimand Name|The literal identifier (i.e., distinctive designation) of the estimand.|||
||label|String|C215524|0..1|Estimand Label|The short descriptive designation for the estimand.|||
||description|String|C215523|0..1|Estimand Description|A narrative representation of the estimand.|||
||notes|CommentAnnotation|C215521|0..*|Estimand Notes|A brief written record relevant to the study estimand.|||
||analysisPopulation|AnalysisPopulation||1||A USDM relationship between the Estimand and AnalysisPopulation classes which provides the details associated with an instance of the analysis population used to partially define a study estimand.|||
||variableOfInterest|Endpoint||1||A USDM relationship between the Estimand and Endpoint classes which provides the details associated with an instance of the variable of interest within a study endpoint used to partially define a study estimand.|||
||intercurrentEvents|IntercurrentEvent||1..*||A USDM relationship between the Estimand and IntercurrentEvent classes which identifies the set of intercurrent events associated with a study estimand.|||
||interventions|StudyIntervention||1..*||A USDM relationship between the Estimand and StudyIntervention classes which identifies the set of study interventions associated with the Estimand.|||
|GeographicScope|||C207591||Geographic Scope|The extent or range related to the physical location of an entity.|||
||id|String||1|||||
||type|Code|C207495|1|Geographic Scope Type|A characterization or classification of the geographic scope.|C207412||
||code|AliasCode|C207494|0..1|Geographic Scope Code|A symbol or combination of symbols which is assigned to the geographic scope.|Point out to external dictionaries: Standard code is ISO-3166; Alias codes drawn from GENC, UN Region Codes, etc.||
|GovernanceDate|||C207595||Study Governance Date|Any of the dates associated with event milestones within a clinical study's oversight and management framework.|||
||id|String||1|||||
||name|String|C207499|1|Study Governance Date Name|The literal identifier (i.e., distinctive designation) of the study governance date|||
||label|String|C207498|0..1|Study Governance Date Label|The short descriptive designation for the study governance date.|||
||description|String|C207497|0..1|Study Governance Date Description|A narrative representation of the study governance date.|||
||type|Code|C207496|1|Study Governance Date Type|A characterization or classification of the study governance date.|C207413||
||dateValue|Date|C207500|1|Study Governance Date Value|The information contained in the date field.|||
||geographicScopes|GeographicScope||1..*||A USDM relationship between the GovernanceDate and GeographicScope classes which identifies the set of geographic scopes associated with the governance date.|||
|HumanName|||||||||
||id|String||1|||||
||text|String||0..1|||||
||family|String||0..1|||||
||given|String||0..*|||||
||prefix|String||0..*|||||
||suffix|String||0..*|||||
|Identifier|||C25364||Identifier|One or more characters used to identify, name, or characterize the nature, properties, or contents of a thing.|||
||id|String||1|||||
||text|String|C215450|1|Identifier Text|An instance of structured text that represents the identifier.|||
||scope|Organization||1||A USDM relationship between the Identifier and Organization classes which provides the details associated with each organization that has assigned the identifier.|||
|Indication|||C41184||Disease/Condition Indication|The disease or condition the intervention will diagnose, treat, prevent, cure, or mitigate.|||
||id|String||1|||||
||name|String|C207503|1|Disease/Condition Indication Name|The literal identifier (i.e., distinctive designation) of the disease/condition indication.|||
||label|String|C207502|0..1|Disease/Condition Indication Label|The short descriptive designation for the disease/condition indication.|||
||description|String|C112038|0..1|Disease/Condition Indication Description|A narrative representation of the condition, disease or disorder that the clinical trial is intended to investigate or address.|||
||isRareDisease|Boolean|C207501|1|Disease/Condition Indication Is Rare Disease Indicator|An indication as to whether the disease/condition indication under study is considered a rare disease.|||
||codes|Code|C188822|0..*|Disease/Condition Indication Code|A short sequence of characters that represents the disease/condition indication.|Point out to multiple Biomedical coding dictionaries such as SNOMEDCT (for FDA), MedDRA, NCIt, ICD's, etc.||
||notes|CommentAnnotation|C215509|0..*|Indication Notes|A brief written record relevant to the disease/condition indication.|||
|Ingredient|||C51981||Ingredient|Any component that constitutes a part of a compounded substance or mixture.|||
||id|String||1|||||
||role|Code|C215595|1|Ingredient Role|The intended use of the ingredient within the context of the compounded substance or mixture.|Point to FHIR value set: Ingredient Role||
||substance|Substance||1||A USDM relationship between the Ingredient and Substance classes that identifies the substance associated with the ingredient.|||
|IntercurrentEvent|||C188815||Intercurrent Event|An event(s) occurring after treatment initiation that affects either the interpretation or the existence of the measurements associated with the clinical question of interest. (ICH E9 Addendum on Estimands)|||
||id|String||1|||||
||name|String|C188855|1|Intercurrent Event Name|The literal identifier (i.e., distinctive designation) of the intercurrent event.||SyntaxTemplate|
||label|String|C207504|0..1|Intercurrent Event Label|The short descriptive designation for the intercurrent event.||SyntaxTemplate|
||description|String|C188856|0..1|Intercurrent Event Description|A narrative representation of the intercurrent event.||SyntaxTemplate|
||text|String|C215526|1|Intercurrent Event Text|An instance of structured text that represents the intercurrent event.||SyntaxTemplate|
||notes|CommentAnnotation|C215527|0..*|Intercurrent Event Notes|A brief written record relevant to the intercurrent event.||SyntaxTemplate|
||dictionary|SyntaxTemplateDictionary||0..1||A USDM relationship between the IntercurrentEvent and SyntaxTemplateDictionary classes which provides the set of dictionary entries related to the intercurrent event. ||SyntaxTemplate|
||strategy|String|C188857|1|Intercurrent Event Strategy|A textual description of the planned strategy to manage and/or mitigate intercurrent events.|||
|InterventionalStudyDesign|||C215503||Interventional Study Design|The strategy that specifies the structure of an interventional trial in terms of the planned activities (including timing) and statistical analysis approach intended to meet the objectives of the study.|||
||id|String||1|||||
||name|String|C215626|1|Interventional Study Design Name|The literal identifier (i.e., distinctive designation) of the interventional study design.||StudyDesign|
||label|String|C215628|0..1|Interventional Study Design Label|The short descriptive designation for the interventional study design.||StudyDesign|
||description|String|C215627|0..1|Interventional Study Design Description|A narrative representation of the interventional study design.||StudyDesign|
||rationale|String|C215629|1|Interventional Study Design Rationale|Reason(s) for choosing the interventional study design. This may include reasons for the choice of control or comparator, as well as the scientific rationale for the study design.||StudyDesign|
||therapeuticAreas|Code|C215633|0..*|Interventional Study Design Therapeutic Areas|A categorization of a disease, disorder, or other condition based on common characteristics and often associated with a medical specialty focusing on research and development of specific therapeutic interventions for the purpose of treatment and prevention, which is associated with the interventional study design.|Point out to external dictionaries|StudyDesign|
||studyType|Code|C215631|0..1|Interventional Study Design Study Type|The study type associated with the interventional study design.|SDTM Terminology Codelist C99077|StudyDesign|
||characteristics|Code|C215632|0..*|Interventional Study Design Characteristics|The distinguishing qualities or prominent aspects of an interventional study design.|C207416|StudyDesign|
||studyPhase|AliasCode|C215630|0..1|Interventional Study Design Study Phase|The study phase associated with the interventional study design.|SDTM Terminology Codelist C66737|StudyDesign|
||notes|CommentAnnotation|C215634|0..*|Interventional Study Design Notes|A brief written record relevant to the interventional study design.||StudyDesign|
||activities|Activity||0..*||A USDM relationship between the InterventionalStudyDesign and Activity classes which identifies the set of activities associated with the interventional study design.||StudyDesign|
||biospecimenRetentions|BiospecimenRetention||0..*||A USDM relationship between the InterventionalStudyDesign and BiospecimenRetention classes which identifies the status of biospecimen retentions related to the interventional study design.||StudyDesign|
||encounters|Encounter||0..*||A USDM relationship between the InterventionalStudyDesign and Encounter classes which identifies the set of encounters associated with the interventional study design.||StudyDesign|
||estimands|Estimand||0..*||A USDM relationship between the InterventionalStudyDesign and Estimand classes which identifies the set of estimands associated with the interventional study design.||StudyDesign|
||indications|Indication||0..*||A USDM relationship between the InterventionalStudyDesign and Indication classes which identifies the set of indications associated with the interventional study design.||StudyDesign|
||objectives|Objective||0..*||A USDM relationship between the InterventionalStudyDesign and Objective classes which identifies the set of objectives associated with the interventional study design.||StudyDesign|
||scheduleTimelines|ScheduleTimeline||0..*||A USDM relationship between the InterventionalStudyDesign and ScheduleTimeline classes which identifies the set of scheduled timelines associated with the interventional study design.||StudyDesign|
||arms|StudyArm||1..*||A USDM relationship between the InterventionalStudyDesign and StudyArm classes which identifies the set of study arms associated with the interventional study design.||StudyDesign|
||studyCells|StudyCell||1..*||A USDM relationship between the InterventionalStudyDesign and StudyCell classes which identifies the set of study cells associated with the interventional study design. ||StudyDesign|
||documentVersions|StudyDefinitionDocumentVersion||0..*||A USDM relationship between the InterventionalStudyDesign and StudyDefinitionDocumentVersion classes which identifies the version of the study definition documents associated with the interventional study design.||StudyDesign|
||elements|StudyElement||0..*||A USDM relationship between the InterventionalStudyDesign and StudyElement classes which identifies the set of study elements associated with the interventional study design.||StudyDesign|
||studyInterventions|StudyIntervention||0..*||A USDM relationship between the InterventionalStudyDesign and StudyIntervention classes which identifies the set of study interventions associated with interventional study design.||StudyDesign|
||epochs|StudyEpoch||1..*||A USDM relationship between the InterventionalStudyDesign and StudyEpoch classes which identifies the set of study epochs associated with the interventional study design.||StudyDesign|
||population|StudyDesignPopulation||1||A USDM relationship between the InterventionalStudyDesign and StudyDesignPopulation classes which identifies the population associated with the interventional study design.||StudyDesign|
||model|Code|C98746|1|Intervention Model Type|The general design of the strategy for assigning interventions to subjects in a clinical study. (clinicaltrials.gov)|SDTM Terminology Codelist C99076||
||subTypes|Code|C49660|0..*|Trial Type|The nature of the interventional study for which information is being collected.|SDTM Terminology Codelist C66739||
||blindingSchema|AliasCode|C49658|0..1|Trial Blinding Schema|The type of experimental design used to describe the level of awareness of the study subjects and/ or study personnel as it relates to the respective intervention(s) or assessments being observed, received or administered.|SDTM Terminology Codelist C66735||
||intentTypes|Code|C49652|0..*|Trial Intent Type|The planned purpose of the therapy, device, or agent under study in the clinical trial.|SDTM Terminology Codelist C66736||
|Masking|||C191278||Masking|The mechanism used to obscure the distinctive characteristics of the study intervention or procedure to make it indistinguishable from a comparator. (CDISC Glossary)|||
||id|String||1|||||
||text|String|C215553|1|Masking Text|An instance of unstructured text that represents how the masking is performed and maintained.|||
||isMasked|Boolean|C215554|1|Masked Indicator|An indication as to whether the study role is masked.|||
|MedicalDevice|||C16830||Medical Device|Any instrument, apparatus, implement, machine, appliance, implant, reagent for in vitro use, software, material or other similar or related article, intended by the manufacturer to be used, alone or in combination for, one or more specific medical purpose(s). [After REGULATION (EU) 2017/745 OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL of 5 April 2017 on medical devices]|||
||id|String||1|||||
||name|String|C215614|1|Medical Device Name|The literal identifier (i.e., distinctive designation) of the medical device.|||
||label|String|C215616|0..1|Medical Device Label|The short descriptive designation for the medical device.|||
||description|String|C215615|0..1|Medical Device Description|A narrative representation of the medical device.|||
||hardwareVersion|String|C215617|0..1|Hardware Version|A form or variant of hardware; one of a sequence of copies of the physical components from which a computer is constructed, each incorporating new modifications.|||
||softwareVersion|String|C111093|0..1|Software Version|A form or variant of software; one of a sequence of copies of a software program, each incorporating new modifications. (NCI)|||
||sourcing|Code|C215619|0..1|Medical Device Sourcing|An indication as to whether the medical device is obtained from a local or central source.|CNEW - Product Sourcing Value Set||
||notes|CommentAnnotation|C215618|0..*|Medical Device Notes|A brief written record relevant to the medical device.|||
||embeddedProduct|AdministrableProduct||0..1||A USDM relationship between the MedicalDevice and AdministrableProduct classes which identifies the administrable product that is an integral component of the medical device.|||
||identifiers|MedicalDeviceIdentifier||0..*||A USDM relationship between the MedicalDevice and MedicalDeviceIdentifier classes which provides the set of identifiers related to the medical device.|||
|MedicalDeviceIdentifier|||C215501||Medical Device Identifier|A sequence of characters used to identify, name, or characterize the medical device.|||
||id|String||1|||||
||text|String|C215620|1|Medical Device Identifier Text|An instance of structured text that represents the medical device identifier.||Identifier|
||scope|Organization||1||A USDM relationship between the MedicalDeviceIdentifier and Organization classes which provides the details associated with each organization that has assigned the identifier.||Identifier|
||type|Code|C215621|1|Medical Device Identifier Type|A characterization or classification of the medical device identifier.|CNEW - Medical Device Identifier Type Value Set||
|NarrativeContent|||C207592||Narrative Content|The container that holds an instance of unstructured text and which may include objects such as tables, figures, and images.|||
||id|String||1|||||
||name|String|C207507|1|Narrative Content Name|The literal identifier (i.e., distinctive designation) of the narrative content.|||
||sectionNumber|String|C207509|0..1|Narrative Content Section Number|The numeric identifier assigned to a particular document section containing narrative content.|||
||sectionTitle|String|C207510|0..1|Narrative Content Section Title|An identifying designation for the document section containing narrative content.|||
||displaySectionTitle|Boolean|C215534|1|Narrative Content Section Title Display Indicator|An indication as to whether the section title is to be displayed in the document containing narrative content.|||
||displaySectionNumber|Boolean|C215535|1|Narrative Content Section Number Display Indicator|An indication as to whether the section number is to be displayed in the document containing narrative content.|||
||contentItem|NarrativeContentItem||0..1||A USDM relationship between the NarrativeContent and NarrativeContentItem classes which identifies the content item associated with the narrative content.|||
||previous|NarrativeContent||0..1||A USDM relationship within the NarrativeContent class which identifies the narrative content that precedes the current narrative content in the display order.|||
||next|NarrativeContent||0..1||A USDM relationship within the NarrativeContent class which identifies the narrative content that follows the current narrative content in the display order.|||
||children|NarrativeContent||0..*||A USDM relationship within the NarrativeContent class which identifies the set of child content associated with an instance of narrative content.|||
|NarrativeContentItem|||C215489||Narrative Content Item|An individual item within the container that holds an instance of unstructured text and which may include objects such as tables, figures, and images.|||
||id|String||1|||||
||name|String|C215557|1|Narrative Content Item Name|The literal identifier (i.e., distinctive designation) of the narrative content item.|||
||text|String|C215558|1|Narrative Content Item Text|An instance of unstructured text that represents the narrative content item.|||
|Objective|||C142450||Study Objective|The reason for performing a study in terms of the scientific questions to be answered by the analysis of data collected during the study.|||
||id|String||1|||||
||name|String|C207512|1|Study Objective Name|The literal identifier (i.e., distinctive designation) of the study objective.||SyntaxTemplate|
||label|String|C207511|0..1|Study Objective Label|The short descriptive designation for the study objective.||SyntaxTemplate|
||description|String|C94090|0..1|Study Objective Description|A narrative representation of the study objective. (BRIDG)||SyntaxTemplate|
||text|String|C207513|1|Study Objective Text|An instance of structured text that represents the study objective.||SyntaxTemplate|
||notes|CommentAnnotation|C215513|0..*|Objective Notes|A brief written record relevant to the study objective.||SyntaxTemplate|
||dictionary|SyntaxTemplateDictionary||0..1||A USDM relationship between the Objective and SyntaxTemplateDictionary classes which provides the set of dictionary entries related to study objectives.||SyntaxTemplate|
||level|Code|C188823|1|Study Objective Level|A characterization or classification of the study objective that determines its category of importance relative to other study objectives.|C188725||
||endpoints|Endpoint||0..*||A USDM relationship between the Objective and Endpoint classes which identifies the set of endpoints associated with the study objective.|||
|ObservationalStudyDesign|||C215504||Observational Study Design|The strategy that specifies the structure of an observational study in terms of the planned activities (including timing) and statistical analysis approach intended to meet the objectives of the study.|||
||id|String||1|||||
||name|String|C215636|1|Observational Study Design Name|The literal identifier (i.e., distinctive designation) of the observational study design.||StudyDesign|
||label|String|C215638|0..1|Observational Study Design Label|The short descriptive designation for the observational study design.||StudyDesign|
||description|String|C215637|0..1|Observational Study Design Description|A narrative representation of the observational study design.||StudyDesign|
||rationale|String|C215639|1|Observational Study Design Rationale|Reason(s) for choosing the observational study design. This may include reasons for the choice of control or comparator, as well as the scientific rationale for the study design.||StudyDesign|
||therapeuticAreas|Code|C215643|0..*|Observational Study Design Therapeutic Areas|A categorization of a disease, disorder, or other condition based on common characteristics and often associated with a medical specialty focusing on research and development of specific therapeutic interventions for the purpose of treatment and prevention, which is associated with the observational study design.|Point out to external dictionaries|StudyDesign|
||studyType|Code|C215641|0..1|Observational Study Design Study Type|The study type associated with the observational study design.|SDTM Terminology Codelist C99077|StudyDesign|
||characteristics|Code|C215642|0..*|Observational Study Design Characteristics|The distinguishing qualities or prominent aspects of an observational study design.|C207416|StudyDesign|
||studyPhase|AliasCode|C215640|0..1|Observational Study Design Study Phase|The study phase associated with the observational study design.|SDTM Terminology Codelist C66737|StudyDesign|
||notes|CommentAnnotation|C215644|0..*|Observational Study Design Notes|A brief written record relevant to the observational study design.||StudyDesign|
||activities|Activity||0..*||A USDM relationship between the ObservationalStudyDesign and Activity classes which identifies the set of activities associated with the observational study design.||StudyDesign|
||biospecimenRetentions|BiospecimenRetention||0..*||A USDM relationship between the ObservationalStudyDesign and BiospecimenRetention classes which identifies the status of biospecimen retentions related to the observational study design.||StudyDesign|
||encounters|Encounter||0..*||A USDM relationship between the ObservationalStudyDesign and Encounter classes which identifies the set of encounters associated with the observational study design.||StudyDesign|
||estimands|Estimand||0..*||A USDM relationship between the ObservationalStudyDesign and Estimand classes which identifies the set of estimands associated with the observational study design.||StudyDesign|
||indications|Indication||0..*||A USDM relationship between the ObservationalStudyDesign and Indication classes which identifies the set of indications associated with the observational study design.||StudyDesign|
||objectives|Objective||0..*||A USDM relationship between the ObservationalStudyDesign and Objective classes which identifies the set of objectives associated with the observational study design.||StudyDesign|
||scheduleTimelines|ScheduleTimeline||0..*||A USDM relationship between the ObservationalStudyDesign and ScheduleTimeline classes which identifies the set of scheduled timelines associated with the observational study design.||StudyDesign|
||arms|StudyArm||1..*||A USDM relationship between the ObservationalStudyDesign and StudyArm classes which identifies the set of study arms associated with the observational study design.||StudyDesign|
||studyCells|StudyCell||1..*||A USDM relationship between the ObservationalStudyDesign and StudyCell classes which identifies the set of study cells associated with the observational study design. ||StudyDesign|
||documentVersions|StudyDefinitionDocumentVersion||0..*||A USDM relationship between the ObservationalStudyDesign and StudyDefinitionDocumentVersion classes which identifies the version of the study definition documents associated with the observational study design.||StudyDesign|
||elements|StudyElement||0..*||A USDM relationship between the ObservationalStudyDesign and StudyElement classes which identifies the set of study elements associated with the observational study design.||StudyDesign|
||studyInterventions|StudyIntervention||0..*||A USDM relationship between the ObservationalStudyDesign and StudyIntervention classes which identifies the set of study interventions associated with observational study design.||StudyDesign|
||epochs|StudyEpoch||1..*||A USDM relationship between the ObservationalStudyDesign and StudyEpoch classes which identifies the set of study epochs associated with the observational study design.||StudyDesign|
||population|StudyDesignPopulation||1||A USDM relationship between the ObservationalStudyDesign and StudyDesignPopulation classes which identifies the population associated with the observational study design.||StudyDesign|
||model|Code|C147138|1|Observation Study Design Model Type|The general design of the strategy for identifying and following up with participants during observational studies. (clinicaltrials.gov)|SDTM Terminology Codelist C127259||
||subTypes|Code|C215635|0..*|Observational Study Type|The nature of the observational study for which information is being collected.|CNEW - Observational Study Type Response||
||timePerspective|Code|C126065|1|Observational Time Perspective|The temporal relationship between the observation period and time of subject enrollment. (ClinicalTrials.gov)|SDTM Terminology Codelist C127261||
||samplingMethod|Code|C126067|0..1|Observational Study Sampling Method|The sampling method used to assign study participants into groups or cohorts within an observational study.|SDTM Terminology Codelist C127260||
|Organization|||C19711||Organization|A formalized group of persons or other organizations collected together for a common purpose (such as administrative, legal, political) and the infrastructure to carry out that purpose. (BRIDG)|||
||id|String||1|||||
||name|String|C93874|1|Organization Name|The literal identifier (i.e., distinctive designation) of the organization.|||
||label|String|C207514|0..1|Organization Label|The short descriptive designation for the organization.|||
||identifier|String|C93401|1|Organization Identifier|A unique symbol that establishes identity of the organization. (BRIDG)|||
||identifierScheme|String|C188819|1|Identifier Provider Organization Name|The name of the organization that provides the identifier for the entity.|||
||type|Code|C188820|1|Organization Type|A characterization or classification of the formalized group of persons or other organizations collected together for a common purpose (such as administrative, legal, political) and the infrastructure to carry out that purpose.|C188724||
||legalAddress|Address||0..1||A USDM relationship between the Organization and Address classes which provides the legal address for an organization.|||
||managedSites|StudySite||0..*||A USDM relationship between the Organization and StudySite classes which identifies the set of study sites managed by the organization.|||
|ParameterMap|||C207456||Parameter Map|The paired name and value for a given parameter.|||
||id|string||1|||||
||tag|String|C207515|1|Programming Tag|Character strings bounded by angle brackets that act as containers for programming language elements.|||
||reference|String|C207516|1|Programming Tag Reference|The reference for a tag used in programming languages, such as a markup language (e.g., HTML, XML), to store attributes and elements.|||
|PopulationDefinition|||C207593||Population Definition|A concise explanation of the meaning of a population.|||
||id|String||1|||||
||name|String|C207520|1|Population Definition Name|The literal identifier (i.e., distinctive designation) of the population definition.|||
||label|String|C207519|0..1|Population Definition Label|The short descriptive designation for the population definition.|||
||description|String|C207517|0..1|Population Definition Description|A narrative representation of the population definition.|||
||plannedSex|Code|C207523|0..2|Population Definition Planned Sex|The protocol-defined sex within the population definition.|SDTM Terminology Codelist C66732||
||includesHealthySubjects|Boolean|C207518|1|Population Definition Includes Healthy Subjects Indicator|An indication as to whether the population definition includes healthy subjects, that is, subjects without the disease or condition under study.|||
||plannedAge|Range|C207701|0..1|Population Definition Planned Age|The anticipated age of subjects within the population definition.|||
||plannedCompletionNumber|QuantityRange||0..1|||||
||plannedEnrollmentNumber|QuantityRange||0..1|||||
||notes|CommentAnnotation|C215551|0..*|Population Definition Notes|A brief written record relevant to the population definition.|||
||criteria|EligibilityCriterion||0..*||A USDM relationship between the PopulationDefinition and EligibilityCriterion classes which identifies the set of eligibility criteria associated with the population definition.|||
|Procedure|||C98769||Procedure|Any activity performed by manual and/or instrumental means for the purpose of diagnosis, assessment, therapy, prevention, or palliative care.|||
||id|String||1|||||
||name|String|C201325|1|Procedure Name|The literal identifier (i.e., distinctive designation) of the procedure.|||
||label|String|C207524|0..1|Procedure Label|The short descriptive designation for the procedure.|||
||description|String|C201324|0..1|Procedure Description|A narrative representation of the procedure.|||
||procedureType|String|C188848|1|Procedure Type|A characterization or classification of the study procedure.|||
||code|Code|C154626|1|Procedure Code|A symbol or combination of symbols which is assigned to medical procedure.|Point out to external dictionary like CPT, MedDRA, SNOMEDCT, etc.||
||notes|CommentAnnotation|C215520|0..*|Procedure Notes|A brief written record relevant to the procedure.|||
||studyIntervention|StudyIntervention||0..1||A USDM relationship between the Procedure and StudyInterventionclasses which provides the details associated with an instance of an intervention performed during the conduct of a procedure.|||
|ProductOrganizationRole|||C215502||Product Organization Role|A designation that identifies the function of an organization within the context of the product.|||
||id|String||1|||||
||name|String|C215622|1|Product Organization Role Name|The literal identifier (i.e., distinctive designation) of the product organization role.|||
||label|String|C215624|0..1|Product Organization Role Label|The short descriptive designation for the product organization role.|||
||description|String|C215623|0..1|Product Organization Role Description|A narrative representation of the product organization role.|||
||code|Code|C215625|1|Product Organization Role Code|A symbol or combination of symbols which is assigned to the product organization role.|||
||appliesTo|AdministrableProduct, MedicalDevice||0..*||A USDM relationship between the ProductOrganizationRole and either the AdministrableProduct or MedicalDevice class that identifies the administrable product or medical device to which the product organization role applies.|||
||organization|Organization||1||A USDM relationship between the ProductOrganizationRole and Organization classes which identifies the organization associated with the product organization role.|||
|Quantity|||C25256||Quantity|How much there is of something that can be measured; the total amount or number.|||
||id|String||1|||||
||value|Float|C25712|1|Quantity Value|A numerical quantity measured or assigned or computed.|||
||unit|AliasCode|C44258|0..1|Quantity Unit|The type of unit of measure being used to express a quantity.|SDTM Terminology Codelist C71620||
|QuantityRange|||||||||
||id|String||1|||||
||quantity|Quantity||0..1|||||
||range|Range||0..1|||||
|Range|||C38013||Range|The difference between the lowest and highest numerical values; the limits or scale of variation.|||
||id|String||1|||||
||minValue|Quantity|C25570|1|Minimum Value|The smallest value in quantity or degree in a set of values.|||
||maxValue|Quantity|C25564|1|Maximum Value|The largest value in quantity or degree in a set of values.|||
||isApproximate|Boolean|C207525|1|Value Range is Approximate Indicator|An indication as to whether the value range is almost, but not quite, exact.|||
|ReferenceIdentifier|||C82531||Reference Identifier|A sequence of characters used to identify, name, or characterize the reference.|||
||id|String||1|||||
||text|String|C215572|1|Reference Identifier Text|An instance of structured text that represents the reference identifier.||Identifier|
||scope|Organization||1||A USDM relationship between the ReferenceIdentifier and Organization classes which provides the details associated with each organization that has assigned the reference identifier.||Identifier|
||type|Code|C215571|1|Reference Identifier Type|A characterization or classification of the reference identifier.|CNEW Reference Identifier Type||
|ResponseCode|||C201347||Response Code|A symbol or combination of symbols representing the response to the question.|||
||id|String||1|||||
||name|String||1|||||
||label|String||1|||||
||isEnabled|Boolean|C201330|1|Response Code Enabled Indicator|An indication as to whether the response code is activated for use within a given usage context.|||
||code|Code|CNEW|1|Response Code Value|The literal value of a response code.|||
|ScheduleTimeline|||C201348||Schedule Timeline|A chronological schedule of planned temporal events.|||
||id|String||1|||||
||name|String|C201334|1|Schedule Timeline Name|The literal identifier (i.e., distinctive designation) of the schedule timeline.|||
||label|String|C207530|0..1|Schedule Timeline Label|The short descriptive designation for the schedule timeline.|||
||description|String|C201332|0..1|Schedule Timeline Description|A narrative representation of the schedule timeline.|||
||entryCondition|String|C201333|1|Schedule Timeline Entry Condition|A logical evaluation on which rests the validity of entry into a schedule timeline.|||
||mainTimeline|Boolean|C201331|1|Main Timeline Indicator|An indication as to whether the timeline or timeline component is part of the central or principal timeline.|||
||instances|ScheduledInstance||0..*||A USDM relationship between the ScheduleTimeline and ScheduledInstance classes which identifies the set of scheduled instances (e.g., scheduled activity instances or scheduled decision instances) associated with the scheduled timeline.|||
||entry|ScheduledInstance||1||A USDM relationship between the ScheduleTimeline and ScheduledInstance classes which defines the entry into a scheduled instance (e.g., scheduled activity instances or scheduled decision instances) for a timeline.|||
||exits|ScheduleTimelineExit||0..*||A USDM relationship between the ScheduleTimeline and ScheduleTimelineExit classes which identifies the set of exits from the scheduled timeline.|||
||timings|Timing||0..*||A USDM relationship between the ScheduleTimeline and Timing classes which identifies the set of timings associated with the scheduled timeline.|||
|ScheduleTimelineExit|||C201349||Schedule Timeline Exit|To go out of or leave the schedule timeline.|||
||id|String||1|||||
|ScheduledActivityInstance|||C201350||Scheduled Activity Instance|A scheduled occurrence of an activity event.|||
||id|String||1|||||
||name|String|C207533|1|Scheduled Activity Instance Name|The literal identifier (i.e., distinctive designation) of the scheduled activity instance.||ScheduledInstance|
||label|String|C207532|0..1|Scheduled Activity Instance Label|The short descriptive designation for the scheduled activity instance.||ScheduledInstance|
||description|String|C207531|0..1|Scheduled Activity Instance Description|A narrative representation of the scheduled activity instance.||ScheduledInstance|
||defaultCondition|ScheduledInstance||0..1||A USDM relationship within the ScheduledActivityInstance class which identifies the default condition within a scheduled activity instance.||ScheduledInstance|
||epoch|StudyEpoch||0..1||A USDM relationship between the ScheduledActivityInstance and StudyEpoch classes which identifies the study epoch associated with a scheduled activity instance.||ScheduledInstance|
||activities|Activity||0..*||A USDM relationship between the ScheduledActivityInstance and Activity classes which identifies the set of activities associated with a scheduled activity instance.|||
||encounter|Encounter||0..1||A USDM relationship between the ScheduledActivityInstance and Encounter classes which defines the subject encounter associated with the ScheduleActivityInstance.|||
||timeline|ScheduleTimeline||0..1||A USDM relationship between the ScheduledActivityInstance and ScheduleTimeline classes which provides the details associated with an instance of a scheduled timeline related to a scheduled activity instance.|||
||timelineExit|ScheduleTimelineExit||0..1||A USDM relationship between the ScheduledActivityInstance and ScheduleTimelineExit classes which provides the details associated with the exit from a timeline related to a scheduled activity instance.|||
|ScheduledDecisionInstance|||C201351||Scheduled Decision Instance|A scheduled occurrence of a decision event.|||
||id|String||1|||||
||name|String|C207536|1|Scheduled Decision Instance Name|The literal identifier (i.e., distinctive designation) of the scheduled Decision instance.||ScheduledInstance|
||label|String|C207535|0..1|Scheduled Decision Instance Label|The short descriptive designation for the scheduled Decision instance.||ScheduledInstance|
||description|String|C207534|0..1|Scheduled Decision Instance Description|A narrative representation of the scheduled Decision instance.||ScheduledInstance|
||defaultCondition|ScheduledInstance||0..1||A USDM relationship within the ScheduledDecisionInstance class which identifies the default condition within a scheduled decision instance.||ScheduledInstance|
||epoch|StudyEpoch||0..1||A USDM relationship between the ScheduledDecisionInstance and StudyEpoch classes which identifies the study epoch associated with a scheduled decision instance.||ScheduledInstance|
||conditionAssignments|ConditionAssignment||1..*||A USDM relationship between the ScheduledDecisionInstance and ConditionAssignment classes which identifies the set of condition assignments associated with a scheduled decision instance.|||
|ScheduledInstance|||C201299||Scheduled Instance|A scheduled occurrence of a temporal event.|||
||id|String||1|||||
||name|String|C207455|1|Scheduled Instance Name|The literal identifier (i.e., distinctive designation) of the scheduled instance.|||
||label|String|C207454|0..1|Scheduled Instance Label|The short descriptive designation for the scheduled instance.|||
||description|String|C207453|0..1|Scheduled Instance Description|A narrative representation of the scheduled instance.|||
||defaultCondition|ScheduledInstance||0..1||A USDM relationship within the ScheduledInstance class which identifies the default condition within a scheduled instance.|||
||epoch|StudyEpoch||0..1||A USDM relationship between the ScheduledInstance and StudyEpoch classes which identifies the study epoch associated with a scheduled instance.|||
|Strength|||C215495||Substance Strength|The content of an substance expressed quantitatively per dosage unit, per unit of volume, or per unit of weight, according to the pharmaceutical dose form of the product.|||
||id|String||1|||||
||name|String|C215590|1|Substance Strength Name|The literal identifier (i.e., distinctive designation) of the substance strength.|||
||label|String|C215592|0..1|Substance Strength Label|The short descriptive designation for the substance strength.|||
||description|String|C215591|0..1|Substance Strength Description|A narrative representation of the substance strength.|||
||numerator|QuantityRange||1|||||
||denominator|Quantity|C80489|0..1|Denominator|The divisor of a fraction.|||
|Study|||C15206||Clinical Study|A clinical study involves research using human volunteers (also called participants) that is intended to add to medical knowledge. There are two main types of clinical studies: clinical trials (also called interventional studies) and observational studies. (CDISC Glossary)|||
||id|String||1|||||
||name|String|C68631|1|Clinical Study Name|The literal identifier (i.e., distinctive designation) of the clinical study.|||
||label|String|C207479|0..1|Clinical Study Label|The short descriptive designation for the clinical study.|||
||description|String|C142704|0..1|Clinical Study Description|A narrative representation of the clinical study.|||
||versions|StudyVersion||0..*||A USDM relationship between the Study and StudyVersion classes which identifies the set of versions associated with the study.|||
||documentedBy|StudyDefinitionDocument||0..*||A USDM relationship between the Study and StudyDefinitionDocument classes signifying that the study is documented in a study definition document.|||
|StudyAmendment|||C207594||Study Amendment|A written description of a change(s) to, or formal clarification of, a study.|||
||id|String||1|||||
||name|String||1|||||
||label|String||1|||||
||description|String||1|||||
||number|String|C207537|1|Study Amendment Number|A string of numerals that uniquely identifies a protocol amendment.|||
||notes|CommentAnnotation|C215538|0..*|Study Amendment Notes|A brief written record relevant to the study amendment.|||
||summary|String|C115627|1|Study Amendment Summary|A short narrative representation describing the changes introduced in the current version of the protocol.|||
||geographicScopes|GeographicScope||1..*||A USDM relationship between the StudyAmendment and GeographicScope classes which identifies the set of geographic scopes associated with the study amendment.|||
||dateValues|GovernanceDate||0..*||A USDM relationship between the StudyAmendment and GovernanceDate classes which provides the set of governance dates associated with the study amendment.|||
||impacts|StudyAmendmentImpact||0..*||A USDM relationship between the StudyAmendment and StudyAmendmentImpact classes which identifies the set of impacts that the study amendment has on the study or study subjects.|||
||enrollments|SubjectEnrollment||0..*||A USDM relationship between the StudyAmendment and SubjectEnrollment classes which provides the set of subject enrollments associated with the study amendment.|||
||secondaryReasons|StudyAmendmentReason||0..*||A USDM relationship between the StudyAmendment and StudyAmendmentReason classes which identifies the set of secondary reasons for issuing the study amendment.|||
||changes|StudyChange||1..*||A USDM relationship between the StudyAmendment and  StudyChange classes which identifies the set of changes associated with the study amendment.|||
||previous|StudyAmendment||0..1||A USDM relationship within the StudyAmendment class which identifies the study amendment that chronologically precedes the current study amendment.|||
||primaryReason|StudyAmendmentReason||1||A USDM relationship between the StudyAmendment and StudyAmendmentReason classes which identifies the primary reason for issuing the study amendment.|||
|StudyAmendmentImpact|||C215500||Study Amendment Impact|The effect or consequence of an amendment on some aspect of the study.|||
||id|String||1|||||
||text|String|C215611|1|Study Amendment Impact Text|An instance of unstructured text that represents the study amendment impact.|||
||isSubstantial|Boolean|C207538|1|Study Amendment Impact Substantial Indicator|An indication as to whether the study amendment's impact on the study is substantial.|||
||type|Code|C215612|1|Study Amendment Impact Type|A characterization or classification of the study amendment impact.|CNEW Study Amendment Impact Type Response||
||notes|CommentAnnotation|C215613|0..*|Study Amendment Impact Notes|A brief written record relevant to the study amendment impact.|||
|StudyAmendmentReason|||C207457||Study Amendment Reason|The rationale for the change(s) to, or formal clarification of, a protocol.|||
||id|String||1|||||
||otherReason|String|C207539|0..1|Other Reason for Study Amendment|The rationale for the change(s) to, or formal clarification of, a protocol that is not otherwise specified.|||
||code|Code|C207540|1|Study Amendment Reason Code|A symbol or combination of symbols which is assigned to the study amendment reason.|C207415||
|StudyArm|||C174447||Study Arm|A planned pathway assigned to the subject as they progress through the study, usually referred to by a name that reflects one or more treatments, exposures, and/or controls included in the path.|||
||id|String||1|||||
||name|String|C170984|1|Study Arm Name|The literal identifier (i.e., distinctive designation) of the study arm.|||
||label|String|C172456|0..1|Study Arm Label|The short descriptive designation for the study arm.|||
||description|String|C93728|0..1|Study Arm Description|A narrative representation of the study arm.|||
||type|Code|C172457|1|Study Arm Type|A characterization or classification of the study arm.|Protocol Terminology Codelist C174222||
||dataOriginType|Code|C188829|1|Study Arm Data Origin Type|A characterization or classification of the study arm with respect to where the study arm data originates.|C188727||
||dataOriginDescription|String|C188828|1|Study Arm Data Origin Description|The textual representation of the study arm data origin.|||
||notes|CommentAnnotation|C215515|0..*|Study Arm Notes|A brief written record relevant to the study arm.|||
||populations|PopulationDefinition||0..*||A USDM relationship between the StudyArm and PopulationDefinition classes which identifies the set of populations associated with the study arm.|||
|StudyCell|||C188810||Study Design Cell|A partitioning of a study arm into individual pieces, which are associated with an epoch and any number of sequential elements within that epoch.|||
||id|String||1|||||
||arm|StudyArm||1||A USDM relationship between the StudyCell and StudyArm classes which identifies the study arm associated with a study cell.|||
||epoch|StudyEpoch||1||A USDM relationship between the StudyCell and StudyEpoch classes which identifies the study epoch associated with a study cell.|||
||elements|StudyElement||1..*||A USDM relationship between the StudyCell and StudyElement classes which identifies the set of study elements associated with the study cell.|||
|StudyChange|||C215498||Study Change|The act of alteration or modification to a study.|||
||id|String||1|||||
||name|String|C215604|1|Study Change Name|The literal identifier (i.e., distinctive designation) of the study change.|||
||label|String|C215606|0..1|Study Change Label|The short descriptive designation for the study change.|||
||description|String|C215605|0..1|Study Change Description|A narrative representation of the study change.|||
||rationale|String|C215608|1|Study Change Rationale|An explanation as to the logical reasons for why a study change has occurred.|||
||summary|String|C215607|1|Study Change Summary|A short narrative representation describing the changes introduced in the current version of the study.|||
||changedSections|DocumentContentReference||1..*||A USDM relationship between the StudyChange and DocumentContentReference class which provides the set of changed document sections related to the study change.|||
|StudyCohort|||C61512||Study Cohort|A group of individuals who share a set of characteristics (e.g., exposures, experiences, attributes), which logically defines a population under study.|||
||id|String||1|||||
||name|String|C207544|1|Study Cohort Name|The literal identifier (i.e., distinctive designation) of the study cohort.||PopulationDefinition|
||label|String|C207543|0..1|Study Cohort Label|The short descriptive designation for the study cohort.||PopulationDefinition|
||description|String|C207542|0..1|Study Cohort Description|A narrative representation of the study cohort.||PopulationDefinition|
||plannedSex|Code|C207541|0..2|Study Cohort Planned Sex|The protocol-defined sex within the study cohort.|SDTM Terminology Codelist C66732|PopulationDefinition|
||includesHealthySubjects|Boolean|C207480|1|Study Cohort Includes Healthy Subjects Indicator|An indication as to whether the study cohort includes healthy subjects, that is, subjects without the disease or condition under study.||PopulationDefinition|
||plannedAge|Range|C207545|0..1|Study Cohort Planned Age|The anticipated age of subjects within the study cohort.||PopulationDefinition|
||plannedCompletionNumber|QuantityRange||0..1|||||
||plannedEnrollmentNumber|QuantityRange||0..1|||||
||notes|CommentAnnotation|C215547|0..*|Study Cohort Notes|A brief written record relevant to the study cohort.||PopulationDefinition|
||criteria|EligibilityCriterion||0..*||A USDM relationship between the StudyCohort and EligibilityCriterion classes which identifies the set of eligibility criteria associated with the study cohort.||PopulationDefinition|
||characteristics|Characteristic||0..*||A USDM relationship between the StudyCohort and Characteristic classes which identifies the set of subject characteristics associated with the study cohort.|||
||indications|Indication||0..*||A USDM relationship between the StudyCohort and Indication classes which identifies the set of indications associated with the study cohort.|||
|StudyDefinitionDocument|||C215490||Study Definition Document|Any physical or electronic document that is related to defining a study or part of a study.|||
||id|String||1|||||
||name|String|C215559|1|Study Definition Document Name|The literal identifier (i.e., distinctive designation) of the study definition document.|||
||label|String|C215561|0..1|Study Definition Document Label|The short descriptive designation for the study definition document.|||
||description|String|C215560|0..1|Study Definition Document Description|A narrative representation of the study definition document.|||
||type|Code|C215564|1|Study Definition Document Type|A characterization or classification of the study definition document.|CNEW Study Definition Document Type||
||templateName|String|C215562|1|Study Definition Document Template Name|The literal identifier (i.e., distinctive designation) of the study definition document template.|||
||language|Code|C215563|1|Study Definition Document Language|The language in which the study definition document is written.|Point out to ISO 639 language value list||
||notes|CommentAnnotation|C215565|0..*|Study Definition Document Notes|A brief written record relevant to the study definition document.|||
||versions|StudyDefinitionDocumentVersion||0..*||A USDM relationship between the StudyDefinitionDocument and StudyDefinitionDocumentVersion classes which identifies the set of versions associated with the study definition document.|||
|StudyDefinitionDocumentVersion|||C215491||Study Definition Document Version|A representation of a particular edition or snapshot of the study definition document as it exists at a particular point in time.|||
||id|String||1|||||
||status|Code|C215567|1|Study Definition Document Status|A condition of the study definition document at a point in time with respect to its state of readiness for implementation.|C188723||
||version|String|C215566|1|Study Definition Document Version Identifier|A sequence of characters used to identify the version of the study definition document.|||
||notes|CommentAnnotation|C215568|0..*|Study Definition Document Version Notes|A brief written record relevant to the study definition document version.|||
||dateValues|GovernanceDate||0..*||A USDM relationship between the StudyDefinitionDocumentVersion and GovernanceDate classes which provides the set of governance dates associated with the study definition document version.|||
||contents|NarrativeContent||0..*||A USDM relationship between the StudyDefinitionDocumentVersion and NarrativeContent classes which identifies the set of narrative content associated with the version of the study definition document.|||
||children|StudyDefinitionDocumentVersion||0..*||A USDM relationship within the StudyDefinitionDocumentVersion class which identifies the set of child documents of a study definition document version.|||
|StudyDesign|||C15320||Study Design|A plan detailing how a study will be performed in order to represent the phenomenon under examination, to answer the research questions that have been asked, and informing the statistical approach.|||
||id|String||1|||||
||name|String|C201338|1|Study Design Name|The literal identifier (i.e., distinctive designation) of the study design.|||
||label|String|C207548|0..1|Study Design Label|The short descriptive designation for the study design.|||
||description|String|C147139|0..1|Study Design Description|A narrative representation of the study design.|||
||rationale|String|C142705|1|Study Design Rationale|Reason(s) for choosing the study design. This may include reasons for the choice of control or comparator, as well as the scientific rationale for the study design.|||
||therapeuticAreas|Code|C101302|0..*|Therapeutic Areas|A categorization of a disease, disorder, or other condition based on common characteristics and often associated with a medical specialty focusing on research and development of specific therapeutic interventions for the purpose of treatment and prevention.|Point out to external dictionaries||
||studyType|Code|C142175|0..1|Study Type|The nature of the investigation for which study information is being collected. (After clinicaltrials.gov)|SDTM Terminology Codelist C99077||
||characteristics|Code|C207547|0..*|Study Design Characteristic|The distinguishing qualities or prominent aspect of a study design.|C207416||
||studyPhase|AliasCode|C48281|0..1|Trial Phase|A step in the clinical research and development of a therapy from initial clinical trials to post-approval studies. NOTE: Clinical trials are generally categorized into four (sometimes five) phases. A therapeutic intervention may be evaluated in two or more phases simultaneously in different trials, and some trials may overlap two different phases. [21 CFR section 312.21; After ICH Topic E8 NOTE FOR GUIDANCE ON GENERAL CONSIDERATIONS FOR CLINICAL TRIALS, CPMP/ICH/291/95 March 1998]|SDTM Terminology Codelist C66737||
||notes|CommentAnnotation|C215508|0..*|Study Design Notes|A brief written record relevant to the study design.|||
||activities|Activity||0..*||A USDM relationship between the StudyDesign and Activity classes which identifies the set of activities associated with the study design.|||
||biospecimenRetentions|BiospecimenRetention||0..*||A USDM relationship between the StudyDesign and BiospecimenRetention classes which identifies the status of biospecimen retentions related to the study design.|||
||encounters|Encounter||0..*||A USDM relationship between the StudyDesign and Encounter classes which identifies the set of encounters associated with the study design.|||
||estimands|Estimand||0..*||A USDM relationship between the StudyDesign and Estimand classes which identifies the set of estimands associated with the study design.|||
||indications|Indication||0..*||A USDM relationship between the StudyDesign and Indication classes which identifies the set of indications associated with the study design.|||
||objectives|Objective||0..*||A USDM relationship between the StudyDesign and Objective classes which identifies the set of objectives associated with the study design.|||
||scheduleTimelines|ScheduleTimeline||0..*||A USDM relationship between the StudyDesign and ScheduleTimeline classes which identifies the set of scheduled timelines associated with the study design.|||
||arms|StudyArm||1..*||A USDM relationship between the StudyDesign and StudyArm classes which identifies the set of study arms associated with the study design.|||
||studyCells|StudyCell||1..*||A USDM relationship between the StudyDesign and StudyCell classes which identifies the set of study cells associated with the study design. |||
||documentVersions|StudyDefinitionDocumentVersion||0..*||A USDM relationship between the StudyDesign and StudyDefinitionDocumentVersion classes which identifies the version of the study definition documents associated with the study design.|||
||elements|StudyElement||0..*||A USDM relationship between the StudyDesign and StudyElement classes which identifies the set of study elements associated with the study design.|||
||studyInterventions|StudyIntervention||0..*||A USDM relationship between the StudyDesign and StudyIntervention classes which identifies the set of study interventions associated with study design.|||
||epochs|StudyEpoch||1..*||A USDM relationship between the StudyDesign and StudyEpoch classes which identifies the set of study epochs associated with the study design.|||
||population|StudyDesignPopulation||1||A USDM relationship between the StudyDesign and StudyDesignPopulation classes which identifies the population associated with the study design.|||
|StudyDesignPopulation|||C142728||Study Design Population|The population within the general population to which the study results can be generalized.|||
||id|String||1|||||
||name|String|C207553|1|Study Design Population Name|The literal identifier (i.e., distinctive designation) of the study design population.||PopulationDefinition|
||label|String|C207550|0..1|Study Design Population Label|The short descriptive designation for the study design population.||PopulationDefinition|
||description|String|C70834|0..1|Study Design Population Description|A narrative representation of the study design population.||PopulationDefinition|
||plannedSex|Code|C207551|0..2|Study Design Population Planned Sex|The protocol-defined sex within the study design population.|SDTM Terminology Codelist C66732|PopulationDefinition|
||includesHealthySubjects|Boolean|C207549|1|Study Design Population Includes Healthy Subjects Indicator|An indication as to whether the study design population includes healthy subjects, that is, subjects without the disease or condition under study.||PopulationDefinition|
||plannedAge|Range|C207450|0..1|Study Design Population Planned Age|The anticipated age of subjects within the study design population.||PopulationDefinition|
||plannedCompletionNumber|QuantityRange||0..1|||||
||plannedEnrollmentNumber|QuantityRange||0..1|||||
||notes|CommentAnnotation|C215512|0..*|Study Design Population Notes|A brief written record relevant to the study design population.||PopulationDefinition|
||criteria|EligibilityCriterion||0..*||A USDM relationship between the StudyDesignPopulation and EligibilityCriterion classes which identifies the set of eligibility criteria associated with the study design population.||PopulationDefinition|
||cohorts|StudyCohort||0..*||A USDM relationship between the StudyDesignPopulation and StudyCohort classes which identifies the set of study cohorts associated with the study design population.|||
|StudyElement|||C142735||Study Design Element|A basic building block for time within a clinical study comprising the following characteristics: a description of what happens to the subject during the element; a definition of the start of the element; a rule for ending the element.|||
||id|String||1|||||
||name|String|C188833|1|Study Design Element Name|The literal identifier (i.e., distinctive designation) of the study design element.|||
||label|String|C207554|0..1|Study Design Element Label|The short descriptive designation for the study design element.|||
||description|String|C188834|0..1|Study Design Element Description|A narrative representation of the study design element.|||
||notes|CommentAnnotation|C215517|0..*|Study Element Notes|A brief written record relevant to the study element.|||
||transitionEndRule|TransitionRule||0..1||A USDM relationship between the StudyElement and TransitionRule classes which provides the details associated with a transition rule used to trigger the end of a study element.|||
||studyInterventions|StudyIntervention||0..*||A USDM relationship between the StudyElement and StudyIntervention classes which identifies the set of study interventions associated with the study element.|||
||transitionStartRule|TransitionRule||0..1||A USDM relationship between the StudyElement and TransitionRule classes which provides the details associated with a transition rule used to trigger the start of a study element.|||
|StudyEpoch|||C71738||Study Epoch|A named time period defined in the protocol, wherein a study activity is specified and unchanging throughout the interval, to support a study-specific purpose.|||
||id|String||1|||||
||name|String|C93825|1|Study Epoch Name|The literal identifier (i.e., distinctive designation) of the study epoch, i.e., the named time period defined in the protocol, wherein a study activity is specified and unchanging throughout the interval, to support a study-specific purpose.|||
||label|String|C207555|0..1|Study Epoch Label|The short descriptive designation for the study epoch.|||
||description|String|C93824|0..1|Study Epoch Description|A narrative representation of the study epoch.|||
||type|Code|C188830|1|Study Epoch Type|A characterization or classification of the study epoch, i.e., the named time period defined in the protocol, wherein a study activity is specified and unchanging throughout the interval, to support a study-specific purpose.|SDTM Terminology Codelist C99079||
||notes|CommentAnnotation|C215516|0..*|Study Epoch Notes|A brief written record relevant to the study epoch.|||
||previous|StudyEpoch||0..1||A USDM relationship within the StudyEpoch class which identifies the study epoch that chronologically precedes the current study epoch.|||
||next|StudyEpoch||0..1||A USDM relationship within the StudyEpoch class which identifies the study epoch that chronologically follows the current study epoch.|||
|StudyIdentifier|||C83082||Study Identifier|A sequence of characters used to identify, name, or characterize the study.|||
||id|String||1|||||
||text|String|C215507|1|Study Identifier Text|An instance of structured text that represents the study identifier.||Identifier|
||scope|Organization||1||A USDM relationship between the StudyIdentifier and Organization classes which provides the details associated with each organization that has assigned the study identifier.||Identifier|
|StudyIntervention|||C207649||Study Intervention|Any agent, device, or procedure being tested or used as a reference or comparator in the conduct of a clinical trial.|||
||id|String||1|||||
||name|String|C207558|1|Study Intervention Name|The literal identifier (i.e., distinctive designation) of the study intervention.|||
||label|String|C207556|0..1|Study Intervention Label|The short descriptive designation for the study intervention.|||
||description|String|C207647|0..1|Study Intervention Description|A narrative representation of the study intervention.|||
||role|Code|C207560|1|Study Intervention Role|The intended use of the trial intervention within the context of the study design.|C207417||
||type|Code|C98747|1|Study Intervention Type|The kind of product or procedure studied in a trial.|SDTM Terminology Codelist C99078||
||codes|Code|C207648|0..*|Study Intervention Code|A symbol or combination of symbols which is assigned to the study intervention.|Point out to multiple Biomedical coding dictionaries such as WHODrug, ATC, UNII, etc.||
||minimumResponseDuration|Quantity|C207557|0..1|Study Intervention Minimum Response Duration|The value representing the minimum amount of time required to meet the criteria for response to study intervention.|||
||notes|CommentAnnotation|C215543|0..*|Study Intervention Notes|A brief written record relevant to the study intervention.|||
||administrations|Administration||0..*||A USDM relationship between the StudyIntervention and AgentAdministration classes which identifies the set of agent administrations associated with the study intervention.|||
|StudyRole|||C215497||Study Role|A designation that identifies the function of study personnel or an organization within the context of the study.|||
||id|String||1|||||
||name|String|C215600|1|Study Role Name|The literal identifier (i.e., distinctive designation) of the study role.|||
||label|String|C215602|0..1|Study Role Label|The short descriptive designation for the study role.|||
||description|String|C215601|0..1|Study Role Description|A narrative representation of the study role.|||
||code|Code|C215603|1|Study Role Code|A symbol or combination of symbols which is assigned to the study role.|CNEW Study Role Code||
||assignedPersons|AssignedPerson||0..*||A USDM relationship between the StudyRole and AssignedPerson classes that identifies the set of individuals that are assigned to fill a particular role within the study.|||
||masking|Masking||0..1||A USDM relationship between the StudyRole and Masking classes which describes the masking associated with the study role.|||
||organizations|Organization||0..*||A USDM relationship between the StudyRole and Organization classes which identifies the set of organizations associated with the study role.|||
||appliesTo|StudyDesign, StudyVersion||0..*||A USDM relationship between the StudyRole and either StudyVersion or StudyDesign classes that identifies the study version or study design to which the study role applies.|||
|StudySite|||C80403||Study Site|The location at which a study investigator conducts study activities.|||
||id|String||1|||||
||name|String|C207566|1|Study Site Name|The literal identifier (i.e., distinctive designation) of the study site.|||
||label|String|C207565|0..1|Study Site Label|The short descriptive designation for the study site.|||
||description|String|C207564|0..1|Study Site Description|A narrative representation of the study site.|||
||country|Code|C170990|1|Country of Study Site|The country in which the study site is located.|Point out to ISO 3166-1 Alpha-3 Country code||
|StudyTitle|||C49802||Study Title|The sponsor-defined name of the clinical study.|||
||id|String||1|||||
||type|Code|C207568|1|Study Title Type|A characterization or classification of the study title.|C207419||
||text|String|C207567|1|Study Title Text|An instance of unstructured text that represents the study title.|||
|StudyVersion|||C188816||Study Version|A plan at a particular point in time for a study.|||
||id|String||1|||||
||versionIdentifier|String|C207570|1|Study Version Identifier|A sequence of characters used to identify, name, or characterize the study version.|||
||businessTherapeuticAreas|Code|C201322|0..*|Business Therapeutic Areas|A therapeutic area classification based on the structure and operations of the business unit.|Point out to external dictionaries||
||rationale|String|C94122|1|Study Rationale|A statement describing the overall rationale of the study. This field describes the contribution of this study to product development, i.e., what knowledge is being contributed from the conduct of this study.|||
||notes|CommentAnnotation|C215539|0..*|Study Version Notes|A brief written record relevant to the study version.|||
||abbreviations|Abbreviation||0..*||A USDM relationship between the StudyVersion and Abbreviation classes which provides the set of abbreviations associated with the study version.|||
||dateValues|GovernanceDate||0..*||A USDM relationship between the StudyVersion and GovernanceDate classes which provides the set of governance dates associated with the study version.|||
||referenceIdentifiers|ReferenceIdentifier||0..*||A USDM relationship between the StudyVersion and ReferenceIdentifier classes which identifies the set of reference identifiers associated with the study version.|||
||amendments|StudyAmendment||0..*||A USDM relationship between the StudyVersion and StudyAmendment classes which identifies the set of study amendments associated with the study version.|||
||documentVersions|StudyDefinitionDocumentVersion||0..*||A USDM relationship between the StudyVersion and StudyDefinitionDocumentVersion classes which identifies the version of the study definition document associated with the study version.|||
||studyDesigns|StudyDesign||0..*||A USDM relationship between the StudyVersion and StudyDesign classes which identifies the set of study designs associated with the study version.|||
||studyIdentifiers|StudyIdentifier||1..*||A USDM relationship between the StudyVersion and StudyIdentifier classes which identifies the set of study identifiers associated with the study version.|||
||titles|StudyTitle||1..*||A USDM relationship between the StudyVersion and StudyTitle classes which identifies the set of study titles associated with the study version.|||
|SubjectEnrollment|||C37948||Subject Enrollment|The act of enrolling subjects into a study. The subject will have met the inclusion/exclusion criteria to participate in the trial and will have signed an informed consent form. (CDISC Glossary)|||
||id|String||1|||||
||name|String|C215540|1|Subject Enrollment Name|The literal identifier (i.e., distinctive designation) of the subject enrollment.|||
||label|String|C215542|0..1|Subject Enrollment Label|The short descriptive designation for the subject enrollment..|||
||description|String|C215541|0..1|Subject Enrollment Description|A narrative representation of the subject enrollment.|||
||quantity|Quantity|C207573|1|Subject Enrollment Quantity Value|The value representing the number of individuals enrolled in a study.|||
||forGeographicScope|GeographicScope||0..1||A USDM relationship between the SubjectEnrollment and GeographicScope classes which identifies the geographic scope to which the subject enrollment applies.|||
||forStudyCohort|StudyCohort||0..1||A USDM relationship between the SubjectEnrollment and StudyCohort classes which identifies the study cohort to which the subject enrollment applies.|||
||forStudySite|StudySite||0..1||A USDM relationship between the SubjectEnrollment and StudySite classes which identifies the study site to which the subject enrollment applies.|||
|Substance|||C45306||Substance|Any matter of defined composition that has discrete existence, whose origin may be biological, mineral or chemical.|||
||id|String||1|||||
||name|String|C215586|1|Substance Name|The literal identifier (i.e., distinctive designation) of the substance.|||
||label|String|C215588|0..1|Substance Label|The short descriptive designation for the substance.|||
||description|String|C215587|0..1|Substance Description|A narrative representation of the substance.|||
||codes|Code|C215589|0..*|Substance Code|A symbol or combination of symbols which is assigned to the substance.|Point out to multiple Biomedical coding dictionaries such as WHODrug, ATC, UNII, etc.||
||strengths|Strength||1..*||A USDM relationship between the Substance and Strength class which provides the values of the strengths of the substance.|||
||referenceSubstance|Substance||0..1||A USDM relationship within the Substance class that identifies the association between two substances, one of which is used as a reference for the other.|||
|SyntaxTemplate|||C207596||Syntax Template|A standardized pattern used for the arrangement of words and phrases to create well-formed, structured sentences.|||
||id|String||1|||||
||name|String|C207577|1|Syntax Template Name|The literal identifier (i.e., distinctive designation) of the syntax template.|||
||label|String|C207576|0..1|Syntax Template Label|The short descriptive designation for the syntax template.|||
||description|String|C207575|0..1|Syntax Template Description|A narrative representation of the syntax template.|||
||text|String|C207578|1|Syntax Template Text|A structured text string containing prescribed text interspersed with user-defined parameter values.|||
||notes|CommentAnnotation|C215536|0..*|Syntax Template Notes|A brief written record relevant to the syntax template.|||
||dictionary|SyntaxTemplateDictionary||0..1||A USDM relationship between the SyntaxTemplate and SyntaxTemplateDictionary classes which provides the dictionary entry associated with a syntax template. |||
|SyntaxTemplateDictionary|||C207597||Syntax Template Dictionary|A reference source that provides a listing of valid parameter names and values used in syntax template text strings.|||
||id|String||1|||||
||name|String|C207581|1|Syntax Template Dictionary Name|The literal identifier (i.e., distinctive designation) of the syntax template dictionary.|||
||label|String|C207580|0..1|Syntax Template Dictionary Label|The short descriptive designation for the syntax template dictionary.|||
||description|String|C207579|0..1|Syntax Template Dictionary Description|A narrative representation of the syntax template dictionary.|||
||parameterMaps|ParameterMap||1..*||A USDM relationship between the SyntaxTemplateDictionary and ParameterMap classes which identifies the set of parameter maps (parameter map entries) associated with a syntax template dictionary.|||
|Timing|||C80484||Timing|The chronological relationship between temporal events.|||
||id|String||1|||||
||name|String|C207584|1|Timing Name|The literal identifier (i.e., distinctive designation) of the timing.|||
||label|String|C207583|0..1|Timing Label|The short descriptive designation for the timing.|||
||description|String|C164648|0..1|Timing Description|A narrative representation of the chronological relationship between temporal events.|||
||type|Code|C201298|1|Timing Type|A characterization or classification of the chronological relationship between temporal events.|C201264||
||relativeToFrom|Code|C201297|1|Timing Relative To From|The name of the reference event used to define the temporal relationship with another event.|C201265||
||value|String|C201341|1|Timing Value|The temporal value of the chronological relationship between temporal events.|||
||valueLabel|String|C207585|1|Timing Value Label|The short descriptive designation for the timing value.|||
||windowLabel|String|C207586|0..1|Timing Window Label|The short descriptive designation for a time period, or other type of interval, during which a temporal event may be achieved, obtained, or observed.|||
||windowLower|String|C201342|0..1|Timing Window, Lower|The earliest chronological value of an allowable period of time during which a temporal event takes place.|||
||windowUpper|String|C201343|0..1|Timing Window, Upper|The latest chronological value of an allowable period of time during which a temporal event takes place.|||
||relativeToScheduledInstance|ScheduledInstance||0..1||A USDM relationship between the Timing and ScheduledInstance classes which identifies the scheduled instance (e.g., scheduled activity instances or scheduled decision instances) to which the timing is relative to.|||
||relativeFromScheduledInstance|ScheduledInstance||1||A USDM relationship between the Timing and ScheduledInstance classes which identifies the scheduled instance (e.g., scheduled activity instances or scheduled decision instances) to which the timing applies.|||
|TransitionRule|||C82567||Transition Rule|A guide that governs the allocation of subjects to operational options at a discrete decision point or branch (e.g., assignment to a particular arm, discontinuation) within a clinical trial plan.|||
||id|String||1|||||
||name|String|C207588|1|Transition Rule Name|The literal identifier (i.e., distinctive designation) of the transition rule.|||
||label|String|C207587|0..1|Transition Rule Label|The short descriptive designation for the transition rule.|||
||description|String|C188835|0..1|Transition Rule Description|A narrative representation of the transition rule.|||
||text|String|C207589|1|Transition Rule Text|An instance of unstructured text that represents the transition rule.|||
