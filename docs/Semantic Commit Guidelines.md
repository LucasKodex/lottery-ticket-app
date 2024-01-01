# Semantic Commit Guidelines

This document is a guideline for semantic commits that SHOULD be used.

## 1. Introduction

This document defines a set of rules for commit messages that help make them semantic.

### 1.1 Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

### 1.2 Augmented Backus-Naur Form

This document uses the Augmented Backus-Naur Form (ABNF) notation of [RFC 5234](https://datatracker.ietf.org/doc/html/rfc5234). 

The following core rules are included by reference as defined in [RFC 5234, Appendix B.1](https://datatracker.ietf.org/doc/html/rfc5234#appendix-B.1): CHAR (any 7-bit US-ASCII character, excluding NUL)

## 2. Commit Rules

### 2.1 Common Definitions

COLON = ":"  

TEXT = *CHAR  

### 2.2 Kinds of Prefix

prefix = "chore"  
prefix =/ "docs"  
prefix =/ "feat"  
prefix =/ "fix"  
prefix =/ "perf"  
prefix =/ "refactor"  
prefix =/ "revert"  
prefix =/ "style"  
prefix =/ "test" 

### 2.3 Commit Message

The commit message must be formed by a \<prefix\>, a colon and then a short and descriptive text.

commit-message = prefix COLON text  

Examples:

- chore: creates project  
- docs: adds readme  
- feat: improves video feature  
- fix: solves issue #13  
- perf: reduces response time  
- refactor: makes route handler more legible  
- revert: rollbacks model changes  
- style: adds a dark theme  
- test: tests the UI  
