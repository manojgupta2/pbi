# Executive Report Plan

## Objective
Create an executive-level Power BI report for defect backlog health, SLA risk, and operational trend management using the actual workbook data.

## Source baseline
- Fact table: FactDefects (1203 rows)
- Project dimension: DimProject (5 rows)
- Date dimension: DimDate (330 rows)
- Priority dimension: DimPriority (4 rows)
- Status dimension: DimStatus (5 rows)
- Benchmark table: ExpectedKPIs (9 rows)
- Aggregate trend table: MonthlyTrend (48 rows)

## Executive goals
- Understand backlog size and trend direction
- Distinguish open and closed defect volumes
- Assess severity and SLA-breach exposure
- Highlight project and team concentration risk
- Support rapid triage without overwhelming the user with unnecessary detail

## Planned pages
1. Executive Defect Health
2. Backlog and SLA Risk
3. Trend and Mix
4. Defect Detail

## Assumptions
- IssueKey is unique in the source workbook.
- ExpectedKPIs is a benchmark table and requires stakeholder confirmation before being treated as a target table.
- DimProject metadata is business-correct in the current model.
- Date values are real dates and should be validated in Desktop before implementation.

## HITL questions
- Should CustomerImpact include Potential as a customer-impacting condition?
- Should Open Defects use OpenFlag only or also include active statuses?
- Is ExpectedKPIs intended as a business target table or as a test oracle for this exercise?
