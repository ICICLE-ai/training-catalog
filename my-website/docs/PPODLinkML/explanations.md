---
tags:
  - Smart-Foodsheds
---

# Explanation

[LinkML](https://linkml.io/) is an emerging standard and toolset for describing data schemas with an orientation towards building linked data applications. LinkML data schemas are written in YAML and the framework provides tools to convert these schemas into a number of other formats, including JSON-Schema, OWL, SQL DDL, SHACL, ShEx, and Python classes.  The framework also provides tools for validating and converting data between different formats including RDF, CSV, JSON, YAML, and SQLite databases.  As such LinkML is intended as a lingua franca for interoperability between data schemas and datasets.

This repository contains two main files, `PPOD.yaml` and `vocabs.yaml`. `PPOD.yaml` contains the classes and slots describing the resources in the Google Sheets document and the RDF file that it generates, and `vocabs.yaml`  gives the enumerated vocabularies that are being used. These enumerated vocabularies include categories such as types of organizations and lists of sustainability issues, ecoregions, and habitat types.

LinkML provides a facility to automatically generate a set of web pages describing the elements in the schema, one web page per element. This has been carried out for the PPOD FSL schema and has been [posted on GitHub Pages](https://ppodschema.github.io/PPOD_FSL/).

Further work on PPOD_FSL will include providing standardized identifiers for newly created data schema elements and instance data using the URL resolution service [w3id.org](https://w3id.org/). Over the near future, work on PPOD schemas will shift to modularizing PPOD into a PPOD core and individual PPOD application schemas that inherit classes and slots from PPOD-core.
