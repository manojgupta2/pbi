# Jira Defect Intelligence Report Specification

## 1. Stakeholder objectives

Primary audience: engineering leadership, QA leads, project managers, and defect triage owners.

The report should help stakeholders:

- Understand the current defect backlog and its operational risk.
- Identify concentration of defects by priority, status, project, component, environment, and assignee.
- Monitor open defects, SLA exposure, customer impact, and aging.
- Track defect creation and closure patterns over time.
- Focus triage discussions on the highest-severity and SLA-breached issues.
- Compare current results with the values present in the `ExpectedKPIs` table where those values are confirmed to be valid targets or test expectations.

The existing PBIP contains a single blank report page (`Page 1`) and no visual, filter, or slicer definitions. This specification is therefore a planning baseline rather than a description of an already-built report.

## 2. Business questions the available data can answer

The model can support these questions, subject to the model improvements listed below:

- How many defect records exist?
- How many defects are open versus closed, using `OpenFlag`, `ClosedFlag`, and `Status`?
- How are defects distributed by `Priority` and severity rank?
- Which statuses contain the most defects?
- Which projects and project codes have the most defects?
- Which components and environments have the greatest defect concentration?
- Which defects are marked as customer-impacting?
- How many defects have breached their SLA, and what is the breached population by priority or project?
- What is the age profile of open defects using `AgeDays`?
- Which assignees have the largest assigned workload?
- How many defects were created by month and priority, using the pre-aggregated `MonthlyTrend` table?
- What are the available expected KPI values in `ExpectedKPIs`, and how do actual KPI measures compare once those expectations are confirmed as targets?

The current model cannot reliably answer date-based questions directly from `FactDefects` because its date fields are `Int64` values and there is no relationship from `FactDefects` to `DimDate`.

## 3. Recommended KPIs

All recommended KPIs below are definitions based only on fields present in the model. They should be implemented as explicit measures, not implicit visual aggregations.

| KPI | Definition supported by the model | Required fields / caveat |
|---|---|---|
| Total defects | Count of defect records, preferably `DISTINCTCOUNT(FactDefects[IssueKey])` if `IssueKey` is unique | `FactDefects[IssueKey]`; validate uniqueness |
| Open defects | Sum of `FactDefects[OpenFlag]` or distinct count of issues filtered to open status | `OpenFlag`, `IssueKey`; confirm flag semantics |
| Closed defects | Sum of `FactDefects[ClosedFlag]` or distinct count of issues filtered to closed status | `ClosedFlag`, `IssueKey`; confirm flag semantics |
| Open defect rate | Open defects divided by total defects | Requires explicit denominator and zero handling |
| SLA-breached defects | Count of defects where `SLABreached` indicates breached | `SLABreached`; confirm the exact value used for breach |
| SLA breach rate | SLA-breached defects divided by total defects or applicable defects | Confirm business denominator |
| Average age of open defects | Average `AgeDays` for open defects | `AgeDays`, `OpenFlag` or `Status`; confirm age calculation date |
| Maximum open age | Maximum `AgeDays` for open defects | `AgeDays`, open-status logic |
| Customer-impacting defects | Count of records where `CustomerImpact` indicates impact | `CustomerImpact`; confirm allowed values |
| High-severity defects | Count of defects in the highest-priority categories, using `DimPriority[SeverityRank]` | Priority ranking and cutoff require stakeholder confirmation |
| Defects by priority | Count of defects grouped by `Priority` | `FactDefects[Priority]` and `DimPriority[Priority]` |
| Defects by status | Count of defects grouped by `Status` | `FactDefects[Status]` and `DimStatus[Status]` |
| Monthly created defects | Sum of `MonthlyTrend[DefectCount]` by `CreatedMonth` and `Priority` | This is a pre-aggregated trend table; reconcile to the issue-level fact before treating as canonical |
| KPI variance to expectation | Actual KPI minus the matching `ExpectedKPIs[ExpectedValue]` | `ExpectedKPIs` is disconnected and its metric names/values need governance confirmation |

## 4. Recommended report pages

### Page 1: Executive Defect Health

Purpose: provide a concise leadership view of backlog size, risk, and movement.

Recommended visuals:

- KPI cards: Total defects, Open defects, Closed defects, SLA-breached defects, customer-impacting defects.
- Stacked column or bar chart: open/closed defects by priority.
- Line chart: defects created by month from `MonthlyTrend`.
- Bar chart: defects by status.
- Detail table: highest-risk defects with `IssueKey`, `Priority`, `Status`, `Summary`, `ProjectName`, `Assignee`, `AgeDays`, `SLABreached`, and `CustomerImpact`.
- Optional KPI target/variance visual only after `ExpectedKPIs` semantics are confirmed.

### Page 2: Backlog and SLA Risk

Purpose: support triage and identify work requiring intervention.

Recommended visuals:

- Bar chart: open defects by priority and project.
- Column chart: SLA-breached defects by priority.
- Histogram or binned column chart: open defects by `AgeDays` bands. Bins may be created in the report/model only after approval.
- Matrix: project by priority with open defects and SLA-breached defects.
- Table: oldest open defects with issue key, summary, assignee, project, priority, age, SLA target, and breach flag.

### Page 3: Trend and Mix

Purpose: analyze when defects are created and how the defect mix changes.

Recommended visuals:

- Line chart: `MonthlyTrend[DefectCount]` by `CreatedMonth`.
- Stacked area or stacked column chart: monthly defects by priority.
- Bar chart: defect mix by component.
- Bar chart: defect mix by environment.
- Small multiples or matrix: monthly trend by priority, if the data volume supports it.

### Page 4: Project and Ownership View

Purpose: compare project workload and assignment concentration.

Recommended visuals:

- Ranked bar chart: total defects by project.
- Ranked bar chart: open defects by assignee.
- Matrix: project, component, and status with defect count.
- Bar chart: customer-impacting defects by project.
- Drill-through-ready issue table for selected project or assignee.

### Page 5: Defect Detail

Purpose: provide a searchable operational record view.

Recommended visuals:

- Table containing `IssueKey`, `Summary`, `ProjectCode`, `ProjectName`, `IssueType`, `Priority`, `Status`, `Component`, `Environment`, `CreatedDate`, `UpdatedDate`, `ResolvedDate`, `Assignee`, `Reporter`, `CustomerImpact`, `SLATargetDays`, `AgeDays`, and `SLABreached`.
- Conditional formatting for priority, status, SLA breach, customer impact, and age.
- Searchable issue-key and summary filters.

## 5. Filters and slicers

### Recommended report-level filters

- Project / project code, after `DimProject` is repaired and related.
- Priority.
- Status.
- Issue type.
- Component.
- Environment.
- Assignee.
- Customer impact.
- SLA breached.
- Created date or created month, after a valid date relationship is added.

### Page-specific filters

- Executive page: priority, status, project, created period.
- SLA page: priority, project, assignee, age band, SLA breached, customer impact.
- Trend page: created month, priority, component, environment.
- Ownership page: project, assignee, component, status.
- Detail page: issue key, summary search, project, priority, status, assignee, SLA breached.

Use dropdown slicers with search for high-cardinality fields such as issue key, summary, assignee, and reporter. Use compact list or tile slicers only for short categorical fields such as priority, status, environment, and customer impact.

## 6. Required semantic-model improvements

### Critical before report implementation

1. **Create a valid date relationship for the issue-level fact.** `FactDefects[CreatedDate]`, `UpdatedDate`, and `ResolvedDate` are `Int64`; `DimDate[Date]` is also `Int64`, but no relationship currently connects them. Convert or expose compatible date keys deliberately, then create an active created-date relationship and inactive updated/resolved relationships if needed for role-playing date analysis.
2. **Repair `DimProject`.** It currently contains only generic columns named `Column1` through `Column4` and has no relationship. Map these columns to their actual business meanings and create a relationship to the fact using a stable project key such as `ProjectCode` if the source supports it.
3. **Replace implicit aggregation with explicit measures.** The model contains zero existing measures. Add the approved KPI measures and set base columns used only through measures to hidden where appropriate.
4. **Validate the source grain and key uniqueness.** Confirm that `FactDefects[IssueKey]` is unique per defect. If it is not, define the grain and use a defensible count strategy.

### Strongly recommended

5. **Disable or remove unnecessary auto-date tables.** The model contains `DateTableTemplate_*` and two `LocalDateTable_*` tables while also containing `DimDate`. This creates duplicate date infrastructure and indicates auto date/time is enabled.
6. **Govern `MonthlyTrend`.** It is a second, pre-aggregated defect table with a relationship only to `DimPriority` and an auto date table. Reconcile it with `FactDefects`; either document it as an aggregate table or derive trends from the issue fact after date modeling is fixed.
7. **Review `ExpectedKPIs`.** It is disconnected, so it cannot automatically filter or compare to actuals. Keep it as a small disconnected target table only if metric names and expected values are governed; otherwise move targets to a governed KPI/target design.
8. **Set date and numeric semantics.** `DimDate[Date]`, year, month number, and other numeric attributes currently use default sum summarization. Set non-additive attributes to `None`; ensure month is sorted by month number and the calendar is marked as a date table.
9. **Hide technical foreign-key columns.** Relationship columns on the many side, especially `FactDefects[Priority]`, `FactDefects[Status]`, and future project/date keys, should be hidden where the dimension fields are the intended user-facing fields.
10. **Add descriptions and business-friendly names.** Visible tables and columns have no descriptions, and `FactDefects` / `Dim*` names are technical. Add descriptions and consider friendly display names while preserving source mappings.
11. **Check high-cardinality fields.** `IssueKey`, `Summary`, `Assignee`, and `Reporter` may be high-cardinality. Keep them for detail/search use, but avoid using them as broad slicers or grouping fields in summary visuals.

## 7. Required measures / DAX

No explicit measures currently exist. The first implementation should add, at minimum:

- `[Total Defects]`
- `[Open Defects]`
- `[Closed Defects]`
- `[Open Defect Rate]`
- `[SLA Breached Defects]`
- `[SLA Breach Rate]`
- `[Average Open Age Days]`
- `[Maximum Open Age Days]`
- `[Customer Impacting Defects]`
- `[High Severity Defects]`
- `[Defect Count]` for use in grouped visuals where a reusable base measure is helpful
- `[Expected KPI Value]` and `[KPI Variance]` only after the `ExpectedKPIs` mapping is confirmed

DAX should not be authored in Phase 1. Before implementation, confirm the exact categorical values for `OpenFlag`, `ClosedFlag`, `SLABreached`, and `CustomerImpact`, and confirm whether issue keys are unique. Date-role measures should be added only after the date relationships are corrected.

## 8. Assumptions and limitations

- The Excel workbook referenced by the model is the source for all imported tables; the report specification does not assume any external data source.
- The meaning of `ProjectCode`, `ProjectName`, and the four generic `DimProject` columns is not fully documented in the model.
- The exact allowed values for status, customer impact, SLA breach, and flags were not encoded as model metadata, so KPI filters require data profiling and stakeholder confirmation.
- `CreatedDate`, `UpdatedDate`, and `ResolvedDate` are stored as `Int64`; the specification does not assume whether they are `YYYYMMDD`, serial dates, or another encoding without source profiling.
- `MonthlyTrend[DefectCount]` is pre-aggregated and may not reconcile automatically with distinct issue counts.
- `ExpectedKPIs` appears to be a test/target table, but the model does not document whether its values are targets, acceptance criteria, or expected sample outputs.
- No report visuals, slicers, page filters, or explicit measures currently exist in the PBIP report definition.
- No assumptions are made about trend direction, SLA policy, severity threshold, or executive alert thresholds.
- No Fabric, Lakehouse, LangGraph, Roo, or external deployment workflow is included in this Phase 1 specification.

## 9. Implementation sequence

1. Profile the imported Excel values and confirm fact grain, issue-key uniqueness, categorical values, date encoding, and `ExpectedKPIs` semantics.
2. Repair the semantic model: project field names and relationship, issue-to-date relationship design, date data types/marking, auto-date cleanup, and technical-column visibility.
3. Add and validate the approved explicit measures; document formats and business definitions.
4. Reconcile `MonthlyTrend` against issue-level fact results and decide whether it remains a governed aggregate table.
5. Build the Executive Defect Health page and validate KPI totals against source data.
6. Build the Backlog and SLA Risk and Trend and Mix pages, validating filter propagation and date behavior.
7. Build the Project and Ownership and Defect Detail pages with searchable operational filters.
8. Validate PBIR structure, visual bindings, relationships, filters, accessibility, and representative totals in Power BI Desktop.
9. Obtain stakeholder approval, then publish or promote the PBIP according to the approved delivery process.

## Dependency status

- Semantic model: local PBIP/TMDL available and inspected read-only.
- Report definition: local PBIR available and inspected read-only.
- Existing report visuals: none found.
- Existing report filters/slicers: none found.
- Existing measures: none found.
- Power BI Desktop rendering: not required for this Phase 1 planning-only task.
- Fabric publishing: out of scope.

## Source inventory

- Project: `powerbi/JiraDefectIntelligence.pbip`
- Semantic model: `powerbi/JiraDefectIntelligence.SemanticModel/definition`
- Report: `powerbi/JiraDefectIntelligence.Report/definition`
- Tables: `FactDefects`, `DimProject`, `DimDate`, `DimPriority`, `DimStatus`, `ExpectedKPIs`, `MonthlyTrend`, plus generated date-support tables.
- Relationships: five existing relationships; none connects `FactDefects` to `DimDate` or `DimProject`.
