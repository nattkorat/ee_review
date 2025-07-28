# Epidemic Event Extraction Evaluation Guidelines

## 1. Introduction

**Event extraction** is a core task in information extraction where structured event information is automatically identified from unstructured text (such as news articles or reports). In the context of **epidemic surveillance**, event extraction helps us track and understand outbreaks, case reports, deaths, and responses related to public health emergencies.

An **event** is defined as a specific incident or occurrence described in the text. Each event typically consists of the following components:

### 1.1 Event Trigger

- The **trigger** is a single word or short phrase that indicates the **occurrence** of an event.
- It is often a **verb or noun** that carries the event’s core meaning.
- Example:  
  - In the sentence *"The Ministry confirmed 50 new cases of measles"*, the trigger is **"confirmed"**, which signals the occurrence of a **CaseReport** event.

### 1.2 Event Type

- Each trigger corresponds to an **event type**, representing the category of the event.
- Examples of event types in epidemic domains include:
  - `Outbreak`, `CaseReport`, `DeathReport`, `Vaccination`, `Prevention`, `TravelAlert`, `Quarantine`

### 1.3 Event Arguments

- Arguments are **entities or attributes** associated with the event. They give details like:
  - **What** happened?
  - **Where**, **when**, **to whom**, or **how many**?
- Each argument is linked to a **role**, such as:
  - `Disease`, `Location`, `Date`, `Agent` (e.g., virus), `VictimCount`, `Organization`, etc.

#### Example:

> **Text**:  
> "In June, the CDC reported 120 cases of cholera in the northern provinces."

| Component     | Value                |
|---------------|----------------------|
| Trigger       | reported             |
| Event Type    | CaseReport           |
| Arguments     | - Date: June  
|               | - Organization: CDC  
|               | - VictimCount: 120 cases  
|               | - Disease: cholera  
|               | - Location: northern provinces  |

By extracting this structured information, we can build knowledge graphs, perform epidemic trend analysis, and improve early warning systems.

---

## 2. Objective

This evaluation task is designed to assess the quality of **LLM-generated epidemic event extraction**. Annotators will verify, correct, or augment the model's outputs, focusing on:

- Event **triggers**
- Event **types**
- Event **arguments** and **roles**

Each document may contain **multiple events**, and each event can contain **multiple arguments**.

---

## 3. Annotator Responsibilities

Annotators are expected to:

1. **Review** all LLM-extracted events.
2. **Verify and correct**:
   - Event triggers
   - Event types
   - Arguments (span and role)
3. **Add** missing but relevant events or arguments.
4. **Remove** unrelated or hallucinated events.
5. **Ensure** events are related to **epidemic or public health topics**.

---

## 4. Evaluation Task Details

### 4.1 Trigger Identification

- **Keep**: Trigger is correct and clearly refers to an epidemic-related event.
- **Edit**: Trigger is partially correct or off by position.
- **Add**: LLM missed a valid event trigger.
- **Remove**: Trigger is incorrect or unrelated to epidemic events.

---

### 4.2 Event Type Classification

- Choose the correct **event type** from a predefined list:

    This will be explained more next time.

  - `Outbreak`, `CaseReport`, `DeathReport`, `Vaccination`, `Prevention`, `TravelAlert`, etc.
- **Edit** if the type does not match the context.

---

### 4.3 Argument Extraction

For each event, check the **arguments**:

- **Correct**: Argument span and role are both accurate.
- **Edit**: Adjust the span or role.
- **Add**: If a relevant argument is missing.
- **Remove**: If hallucinated or irrelevant.

Common **argument roles**:
- `Disease`
- `Location`
- `Date`
- `VictimCount`
- `Agent` (virus/bacteria)
- `Organization`
- `Treatment`

---

### 4.4 Irrelevant Events

- **Remove** any event that is not related to public health or epidemic topics.

---

## Interface Action Summary

| Action       | Description                                            |
|--------------|--------------------------------------------------------|
| Approve    | Confirm trigger, type, and arguments are all correct   |
| Edit       | Fix incorrect spans, types, or argument roles         |
| Add        | Add missing event triggers, arguments, or roles       |
| Remove     | Delete hallucinated or unrelated items                |

---

## 5. Ground Truth Construction via Voting

To ensure a **reliable final annotation**:

1. Each document is reviewed by **3 to 5 annotators**.
2. For each item (trigger, type, argument):
   - Accept the version with **majority agreement** (≥ 3).
3. If there is no consensus:
   - Mark for **manual adjudication** by a domain expert.
4. Use this final version as the **Ground Truth** for evaluation.

---

## 6. Metrics for Post-Evaluation

You may later compute:

- **Precision / Recall / F1** for:
  - Trigger identification
  - Event type classification
  - Argument role extraction

- **Inter-Annotator Agreement**:
  - Cohen’s / Fleiss’ Kappa for categorical decisions
  - Span overlap for token-based matching

- **Correction Stats**:
  - % of items added / removed / edited
  - Most frequent error types

---

## 7. Annotator Tips

- Always read the **entire document context** before making judgments.
- Focus only on **epidemic or disease-related** events.
- When marking spans, be **precise** — no extra punctuation or unnecessary tokens.
- If unsure, leave a **comment** for clarification.
- Events and arguments must be **explicitly stated** in the text (not inferred).

---

## 8. Example

> **Text**:  
> "On Monday, Cambodia reported 125 new cases of dengue fever in Phnom Penh."

**LLM Output**:
- Trigger: `reported` ✅  
- Event Type: `CaseReport` ✅  
- Arguments:
  - Date: `Monday` ✅  
  - Disease: `dengue fever` ✅  
  - Location: `Phnom Penh` ✅

✅ This is correct — approve and move on.

---
