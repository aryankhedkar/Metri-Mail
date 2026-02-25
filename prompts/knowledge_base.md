# Metris Knowledge Base Reference

Use this knowledge when answering customer questions. Link to https://supportmetris.vercel.app/ when relevant.

## Article 1: Getting started with Metris

### Logging in

Go to admin.metrisenergy.com and enter the email and password provided in your welcome email. If you have not received a welcome email, contact your account manager or email support@metrisenergy.com.

### Setting your password

The first time you log in, you will be prompted to set your own password. Choose something secure. If you ever forget it, click Forgot Password on the login page and a reset link will be sent to your email.

### What you see after logging in

You land on your portfolio dashboard. This shows all your sites at a glance with their current status. Each site has a colour-coded indicator:
- Green (Active): Site operating normally
- Orange (Anomaly): Unusual patterns that may need investigation
- Red (Alert): Active alert requiring action

### Finding your way around

The main navigation gives you access to:
- Dashboard: Portfolio overview with generation, PR, and availability metrics
- Sites: Click any site to see its detailed performance, equipment, and alerts
- Alerts: All active and recent alerts across your portfolio
- O&M: Tickets for tracking maintenance and issue resolution
- Reports: Generate performance summaries for any date range
- Invoices: Billing and invoice management

### Need help?

If anything looks unexpected or you are unsure where to find something, your account manager is here to help. You can also email support@metrisenergy.com at any time.
${callout('action','Recommended Action','Spend 10 minutes clicking around the dashboard and opening a couple of sites. Getting familiar with the layout is the best way to start.')}

---

## Article 2: How data flows into Metris

### The three data sources

Metris aggregates data from three independent sources to give you a complete picture of each site.

Inverter monitoring systems are the primary source of generation data. We connect to manufacturer portals (SolarEdge, Huawei, Solis, GoodWe, SMA, and others) via their APIs.

Export meters provide billing-grade data. For sites with half-hourly meters, we pull readings from your supplier or metering agent. This is the data used for revenue calculations.

Weather data comes from SolarGIS, a satellite-based service that measures solar radiation specific to your site's exact location, orientation, and tilt angle.

### How often data updates
- Inverter data: Every 15 to 60 minutes, depending on the manufacturer
- Meter data: Daily (half-hourly readings typically arrive the next day)
- Weather data: Hourly
- Alerts: Raised by your inverters and meters (OEM systems) and displayed in Metris; they clear automatically when the issue is resolved at the equipment.
${callout('note','Note','There is always a small delay between real-world events and data appearing in Metris. If an inverter goes offline at 2pm, you might not see it reflected until 2:15 to 2:30pm. This is normal.')}
### Data quality checks

Metris automatically flags potential data quality issues including missing readings, values outside expected ranges, mismatches between generation and export, and timestamp inconsistencies.

### When data sources disagree

Metris follows a hierarchy: fiscal meter data takes priority for billing, inverter data takes priority for equipment health monitoring, and weather data provides the independent baseline for performance calculations.
${callout('action','Recommended Action','If you are adding new sites, make sure monitoring is fully operational and reporting to the manufacturer portal before requesting Metris integration.')}

---

## Article 3: Self-serve site onboarding

### Before you start

Make sure the following are in place:
- The inverter monitoring system is installed and reporting data to the manufacturer's portal
- You have the API credentials or portal login details
- You know the site's installed capacity (kWp), location, and panel orientation

### Adding a new site
- Navigate to Platform → Sites → Add new site
- Enter site details: name, address, installed capacity, and panel configuration
- Select the inverter manufacturer and enter the API credentials
- Click Publish to create the site

Once published, Metris connects to the monitoring system and begins pulling data. Historical data is backfilled where the manufacturer's API supports it.

### What happens next
- Confirms the API connection is working
- Verifies data is flowing for each piece of equipment
- Sets up weather data for the site's location
- Configures default performance targets

### Common onboarding issues

Wrong credentials: Double-check the API key matches exactly what is in the manufacturer portal. Some systems use a separate API account.

Equipment not reporting: Confirm data appears in the manufacturer portal first.

Missing site details: Capacity and location are required for PR calculations.
${callout('action','Recommended Action','If you run into issues during onboarding, contact your account manager with the site name, manufacturer, and a description of what you are seeing. We can usually resolve connection issues within 24 hours.')}

---

## Article 4: Understanding Performance Ratio (PR)

### What Performance Ratio tells you

Performance Ratio answers a simple question: given the amount of sunlight that hit your panels, how much of that energy did your system capture?

It is expressed as a percentage. If your PR is 80%, your system captured 80% of the energy it theoretically could have produced. The remaining 20% is lost to real-world factors like temperature, cable resistance, inverter efficiency, shading, and soiling.

PR is the single best metric for comparing solar sites because it strips out the variable that differs most between them: weather.

### How we calculate it

Metris supports two methodologies. Your account will be configured to use whichever method your contracts specify.

### Standard PR
Standard PR = Actual Generation ÷ Expected Generation (SolarGIS)
Expected generation from SolarGIS already factors in losses from temperature, shading, module degradation, inverter efficiency, and soiling. It also accounts for your array's specific azimuth, location, slope, and capacity. Because these losses are already built into the denominator, Standard PR can theoretically reach 100%. Target PR is constant throughout the year and typically set above 90%.

### Ideal PR
Ideal PR = Actual Generation ÷ (GTI × Array Capacity)
GTI (Global Tilted Irradiance) is the total solar energy hitting your panels, measured in kWh/m². Multiplied by your array capacity, this gives the theoretical maximum output if every photon converted perfectly with zero losses. Because real-world losses always exist, Ideal PR should never reach 100% in practice. Target PR varies by month (calculated by design software) and is typically below 90%.

When using Ideal PR, Metris requires a target PR value for each month of the year to account for seasonal variation in losses.
${callout('note','Which method is right for me?','Check your PPA or investment documentation. Standard PR is more intuitive for day-to-day monitoring. Ideal PR is common in contractual settings.')}
### Technical PR vs Contractual PR

Technical PR includes all intervals with no exclusions. Useful for O&M contractors.

Contractual PR removes exclusion periods from both numerator and denominator. Used for PPA compliance and investor reporting.
${callout('important','Interpreting the gap','If your Technical PR is 75% but Contractual PR is 88%, significant excluded events occurred. While PPA guarantees are being met, the site experienced substantial downtime from external factors.')}
### What is a "good" PR?
RangeRatingInterpretation90%+ExcellentSystem performing close to expectations80–90%TypicalWell-maintained commercial rooftop systems in the UK70–80%Below expectationsWorth investigatingBelow 70%UnderperformingRequires immediate attention${callout('note','Seasonal note','PR naturally varies with seasons. Summer PR is typically lower than winter because panels lose efficiency as they heat up. Compare against the same month in previous years.')}
### Why PR might look unexpected
- Shading: Trees, buildings, or equipment casting shadows
- Soiling: Dirty panels reduce output without triggering alerts
- Capacity mismatch: Rated capacity in Metris differs from installed
- Curtailment: Export limits reduce actual output (see Article 11)
- Data quality: Missing data from one inverter pulls down the whole site
${callout('action','Recommended Action','If PR drops suddenly or is consistently below target for two or more consecutive months, raise a ticket with your O&M provider. Include the affected period and any coinciding alerts.')}

---

## Article 5: Understanding availability

### What availability tells you

Availability answers: when conditions were right for generation, did your inverters produce power? It focuses purely on whether hardware did its job, making it the key metric for equipment reliability.

### The formula
Availability = Time with energy output ÷ (Total test time − Excluded downtime)- Time with energy output: Intervals where irradiance > 100 W/m² AND inverter reported generation > 0 kWh
- Total test time: All intervals where irradiance exceeded 100 W/m²
- Excluded downtime: Grid issues, DNO limits, force majeure, extreme weather, planned maintenance, or manufacturer delays

### The 100 W/m² threshold

Below 100 W/m² of weighted irradiance, it is too cloudy or too close to sunrise/sunset to fairly expect generation. Night hours are excluded entirely. This threshold ensures your equipment is never penalised for conditions that would make any inverter struggle, regardless of brand or condition.

### How we weight irradiance

Not all arrays are equal. A 500 kW array matters more than a 50 kW array when calculating site-level irradiance, so Metris weights the GTI from each array by its capacity:
Weighted Irradiance = Sum of (GTI × Array Capacity) ÷ Total Capacity
This gives a single irradiance figure for the site that properly represents overall conditions.

### How we track individual inverters

Each inverter is tracked independently for each interval. If a site has ten inverters and one fails for an entire day, availability is roughly 90%, not 0%. One underperformer shows up proportionally, not catastrophically.

### Interval-level precision

Availability is calculated at the native data interval of your monitoring system, typically 5 or 15 minutes. A 15-minute communication dropout looks very different from a 4-hour outage, and the calculation reflects that distinction. When aggregating to daily, monthly, or yearly figures, Metris sums the numerators and denominators separately, then divides. This preserves accuracy much better than averaging percentages.

### Portfolio-level availability

When viewing availability across multiple sites, results are weighted by capacity. A 1 MW site has twice the influence of a 500 kW site in your portfolio average, reflecting the fact that larger sites represent more generation at risk.

### Worked example

Site with 10 inverters on a January day. Irradiance exceeds 100 W/m² for 32 of 40 potential intervals:
- Denominator: 32 intervals × 10 inverters = 320 possible production events
- Numerator: 304 instances where an inverter reported production
- Availability: 304 ÷ 320 = 95.0%

### Interpretation guide
RangeRatingInterpretation95%+HealthyEquipment running well. Minor data gaps are normal.90–95%InvestigateUsually communication problems or intermittent faults.80–90%Attention neededFailed inverter, persistent comms issues, or misconfiguration.Below 80%Significant issuesMajor equipment failure or fundamental data issues.
### Availability vs PR: using both together

High availability with low PR means equipment is running but underperforming. Investigate shading, soiling, degradation, or curtailment.

Low availability with normal PR suggests communication issues rather than actual equipment problems.
${callout('action','Recommended Action','If availability drops below 90% for a full month, investigate. Start by checking inverter logs for fault codes, then verify communication stability.')}

---

## Article 6: Generation vs export: why the numbers differ

### The basics

Generation is total electricity produced, measured at the inverter. Export is electricity flowing back to the grid, measured at the export meter.
Export = Generation − On-site ConsumptionSelf-Consumption = Generation − Export
### Why they differ

On-site consumption is the most common reason. If the building uses some solar electricity directly, it never reaches the export meter.

System losses account for 1 to 3%. Energy is lost in cables and transformers.

Curtailment reduces output at the inverter level to stay within grid limits.

Measurement accuracy: Small discrepancies of 1 to 2% between inverters and fiscal meters are expected.
${callout('tip','Rule of thumb','Export being 1 to 5% lower than generation is normal for sites with any on-site consumption. Larger or inconsistent discrepancies warrant investigation.')}
### Which number should you use?
- For billing and revenue: Always use export meter data
- For system health: Generation data from inverters
- For PR calculations: Check what your PPA specifies
${callout('action','Recommended Action','If export is consistently more than 5% below generation and the site has minimal on-site consumption, investigate potential metering issues or excessive cable losses.')}

---

## Article 7: Irradiance: what it is and why it matters

### Why irradiance matters

Irradiance is the amount of solar energy reaching your panels. Without it, you cannot determine whether low generation is caused by equipment problems or simply less sunshine.

### Two related terms

Irradiance (W/m²) is instantaneous power per area. Think of it as "how bright is the sun right now?"

Irradiation (kWh/m²) is cumulative energy per area over a period. Think of it as "how much total sunlight hit the panels today?"
${callout('tip','Simple rule','When checking a threshold at a single moment, you use W/m². When calculating performance over a period, you use kWh/m².')}
### Where Metris uses irradiance
- Performance Ratio: Standard PR uses SolarGIS expected generation (which incorporates GTI); Ideal PR uses GTI × capacity directly
- Irradiance-based generation: GTI × Capacity × Target PR
- Generation performance chart: Expected vs actual with confidence bands
- Availability: 100 W/m² threshold

### Global Tilted Irradiance (GTI)

GTI accounts for your panels' exact tilt, orientation, and location. Metris sources this from SolarGIS using satellite imagery.
${callout('action','Recommended Action','No direct action needed. Understanding irradiance helps you interpret why PR and availability vary by season.')}

---

## Article 8: Understanding your portfolio dashboard

### Portfolio-level metrics

Generation metric shows total energy generated across your portfolio for the selected period. The delta indicator compares against the previous equivalent period.

Performance Ratio metric displays your actual PR and your target PR. The gap tells you how the portfolio is performing.

### Generation comparison chart
- Self-consumption (energy consumed on-site)
- Export (energy sent to the grid)
- Budget generation (from financial models)
- Irradiance-based generation (GTI × Capacity × Target PR)
${callout('tip','Tip','The irradiance-based generation line adjusts for actual weather. If a month had poor sunshine, the line drops accordingly, so you can see whether your actual generation tracked with weather or fell short for other reasons.')}
### Site map

Geographic view with colour-coded status indicators. Green = normal, orange = anomalous patterns, red = active alert.

### Solar consumed vs exported

The donut chart shows the self-consumption vs export ratio. Self-consumed energy avoids import costs, which are typically higher than export tariff rates.

### Generation performance chart (site level)
- Expected generation line from SolarGIS
- Grey band: SolarGIS confidence interval (80% confidence; the upper and lower bounds each represent 90% confidence intervals)
- Actual generation dots
- Percentage shown: The Performance Ratio
${callout('action','Recommended Action','Focus on sites where actual generation falls outside the confidence band or where PR is below target. These need investigation first.')}

---

## Article 10: Why is there missing data for my site?

### Where data comes from

Metris pulls data from your inverters' monitoring systems via API. If anything disrupts this chain, data gaps appear.

### Common causes

Connectivity issues at site are the most common cause. The internet connection is down, the router has failed, or a SIM card has expired.

Monitoring system outages happen occasionally. Manufacturer platform issues affect all connected sites.

API credential changes break the connection silently.

New equipment not yet configured in Metris.
${callout('tip','Good news','Data is rarely lost permanently. Most monitoring systems store data locally on the inverter and will backfill gaps automatically once connectivity is restored.')}
### How to diagnose the issue

Step 1: Check the manufacturer portal. If data is there but not in Metris, the issue is on our integration side.

Step 2: Check site connectivity. Verify the router/modem is powered on.

Step 3: Contact Metris with the site name and date range affected.
${callout('action','Recommended Action','Check the manufacturer portal first. If data is there but not in Metris, contact your account manager with the site name and the date range affected.')}

---

## Article 11: How does export curtailment affect my numbers?

### What is export curtailment?

Some sites have grid connection agreements (like G100) that limit how much power can be exported. When your system could produce more than this limit, the excess is curtailed.

### How it affects your data

PR looks artificially low because actual output is reduced but expected output is not adjusted.

Generation and export mismatch grows on sunny days.

### Spotting curtailment in your data
- Export flatlines at a consistent level during peak sun hours
- Generation exceeds export by a wider margin on sunny days vs cloudy days
- PR drops specifically on the sunniest days (opposite of what you would expect)
${callout('important','Important','For Metris to handle curtailment properly, your account manager needs to know the export limit from your grid connection agreement. Without this, curtailed output looks identical to underperformance.')}
### How Metris handles curtailment

For sites with known export limits, Metris can flag when curtailment is likely occurring, calculate adjusted performance, and show estimated lost revenue.
${callout('action','Recommended Action','If your site has an export limit not yet reflected in Metris, send your account manager the G100 agreement or export limit value.')}

---

## Article 12: What are exclusions and how do they affect my data?

### What exclusions do

Exclusions remove specific time periods from performance calculations. When a period is excluded, it is removed from both the numerator and denominator of your PR and availability calculations.

### Why exclusions matter

Without exclusions, your performance data would be unfairly penalised for things outside your control. Most PPAs specify which types of events can be excluded.

### Types of exclusions
- Grid outages: DNO takes the grid offline
- Force majeure: Extreme weather, flooding, etc.
- Contractual curtailment: G100 or similar agreements
- Planned maintenance: Scheduled work requiring system offline
${callout('important','For investor reports','If your Technical PR is 75% but Contractual PR is 88%, the exclusions account for that 13-point gap. Both numbers are accurate; they just answer different questions.')}
### How to view exclusions

On any site's performance page, excluded periods appear as shaded regions on the timeline. Click on any exclusion to see the details.
${callout('action','Recommended Action','If you notice a period where performance dropped due to an external event and you have documentation, contact your account manager. The sooner exclusions are applied, the more accurate your reporting.')}

---

## Article 13: Understanding fault alerts and what action to take

### How alerts work

Alerts are raised by your inverters and meters (OEM systems), not by Metris. Metris pulls them from the manufacturer monitoring systems and displays them in one place. Each row in the Alerts tab shows the site, asset type, serial number, alert message (as reported by the OEM), raised date, connection status, and status (Active or Inactive). When the issue is fixed at the inverter or meter side, the alert clears automatically in Metris.

### Common alert messages

Alert text comes from the OEM. Typical examples include:

Network connection error / Communication loss: The device has stopped communicating with the OEM server.

Inverter offline: The inverter is not reporting production.

No action required: Informational; the OEM indicates no immediate action is needed.

Exact wording varies by manufacturer (Huawei, SolarEdge, SMA, etc.).

### Alert statuses

Active: The issue is still open. You can create an O&M ticket to assign and track resolution.

Inactive: The alert has been resolved (typically because the OEM reported the issue as cleared).

### What to do when you see an alert
- Step 1: Open the alert for full context (site, asset, message)
- Step 2: Check whether it is brief (e.g. network blip) or persistent
- Step 3: For persistent alerts, use "Create ticket" to assign to your O&M provider
- Step 4: When the issue is fixed at the equipment, the alert will clear automatically in Metris
${callout('action','Recommended Action','For alerts that last more than 24 hours, create an O&M ticket so resolution is tracked. Critical issues (e.g. site fully offline) should be escalated to your O&M provider immediately.')}

---

## Article 14: How to read your monthly performance report

### Report overview

Your monthly report provides a comprehensive view of portfolio performance, designed to meet investor reporting requirements.

### Executive summary
- Total generation: Energy produced this month (MWh)
- Portfolio PR: Capacity-weighted average Performance Ratio
- Availability: Portfolio-level equipment reliability
- Revenue estimate: Projected earnings

These are compared against the same month last year and against targets.

### Site-by-site breakdown

Each site gets a row showing generation actual vs expected, PR, availability, and active alerts. Sorted by performance deviation.
${callout('tip','Tip','If a site shows strong generation but low PR, check capacity or weather data configuration. If high availability but low generation, investigate curtailment or shading.')}
### Trend analysis

Month-over-month generation comparison, PR trend with seasonal context, and year-to-date performance against targets. Helps spot gradual degradation.

### Incident log

A summary of all alerts, O&M tickets, and maintenance activities. Provides the audit trail investors typically require.
${callout('action','Recommended Action','Review your report within the first week of each month. Flag anomalies to your account manager before sharing with investors.')}

---

## Article 15: Feed-in Tariff revenue and savings explained

### Why FiT sites are special

Sites registered under the Feed-in Tariff earn a generation tariff on every kWh produced, regardless of whether energy is used on-site or exported.

### The three revenue streams

### Generation tariff

Paid on every kWh generated. The most valuable component for most FiT sites.
Generation Tariff Revenue = Total Generation (kWh) × FiT Generation Rate (p/kWh)
### Export tariff

Paid on electricity sent to the grid. Often "deemed" at 50% of generation if no export meter is installed.
Export Tariff Revenue = Export (kWh) × FiT Export Rate (p/kWh)
### Self-consumption savings

Grid electricity you did not have to buy. Valued at your import electricity rate.
Self-Consumption Savings = Self-Consumption (kWh) × Avoided Import Rate (p/kWh)
### Total value calculation
Total Value = Generation Tariff + Export Tariff + Self-Consumption Savings${callout('note','Tariff rates','FiT rates depend on when the system was registered and installation size. Rates are indexed annually by RPI. Your account manager can confirm exact rates for each site.')}
### Tariff rates

Your account manager can confirm the exact rates applicable to each of your sites.
${callout('action','Recommended Action','If your FiT site data does not show all three revenue streams, confirm with your account manager that tariff rates and deemed export percentage have been configured.')}

---

## Article 16: Glossary of solar terms

### Terms A–Z
AvailabilityThe percentage of time equipment produced power when irradiance conditions were sufficient (above 100 W/m²).AzimuthThe compass direction your solar panels face, measured in degrees from north.Contractual PRPerformance Ratio calculated with exclusion periods removed. Used for PPA compliance.CurtailmentIntentional reduction of solar output to comply with grid export limits.Deemed exportAn assumed percentage of generation (typically 50%) counted as export when no export meter is installed.DNODistribution Network Operator. The company responsible for the local electricity grid.Exclusion periodA time period removed from performance calculations because underperformance was caused by external factors.ExportElectricity generated by your solar system that flows back to the grid.Feed-in Tariff (FiT)A UK government scheme that pays solar system owners for every kWh generated plus exported electricity.Force majeureExtraordinary events beyond anyone's control that may be excluded from performance calculations.G100A grid connection agreement that limits the maximum power a site can export.GenerationTotal electricity produced by your solar panels, measured at the inverter output.GTIGlobal Tilted Irradiance. Solar energy hitting your panels, accounting for tilt and orientation.Ideal PRPR calculated using raw irradiance multiplied by capacity. Targets vary monthly.InverterEquipment that converts DC electricity from solar panels into AC electricity.IrradianceInstantaneous solar power per unit area, measured in W/m².kWpKilowatt peak. Rated output of a solar system under Standard Test Conditions.MWhMegawatt hour. 1,000 kWh. Standard unit for commercial solar generation.O&MOperations and Maintenance. The contractor responsible for maintaining your equipment.Performance Ratio (PR)The ratio of actual energy output to expected output, expressed as a percentage.PPAPower Purchase Agreement. A contract specifying price per kWh and performance guarantees.Self-consumptionSolar electricity generated and used on-site. Calculated as Generation minus Export.SolarGISSatellite-based service providing irradiance data specific to each site location.Standard PRPR using SolarGIS expected generation as the denominator. Target is constant year-round.STCStandard Test Conditions. 1 kW/m² irradiance and 25°C cell temperature.Technical PRPR across all intervals with no exclusions. Shows raw equipment performance.Weighted irradianceIrradiance averaged across arrays, weighted by capacity.Carbon intensityThe amount of CO₂ emitted per kWh of electricity from the grid. Metris uses 0.207074 kg CO₂/kWh as the UK default.Embodied carbonThe CO₂ emitted during manufacturing and installing solar panels. Default: 800 kg CO₂ per kW capacity.Invoice cycleA billing period defined by start and end dates, used to generate invoices for selected sites.OEMOriginal Equipment Manufacturer. Refers to inverter and meter manufacturers (SolarEdge, Huawei, SMA, etc.).OAuthAn authentication protocol used by some OEMs (Huawei, Sungrow) that requires logging into their portal to grant Metris access.SPVSpecial Purpose Vehicle. A separate legal entity often used to hold solar assets for financing purposes.ContactA customer user account in Metris that accesses the Customer Portal, as opposed to a User who accesses the Manage Platform.

---

## Article 18: Connecting OEM integrations

### Supported manufacturers

Metris integrates with all major inverter and meter manufacturers used in commercial solar:
- SolarEdge: API key from SolarEdge Monitoring Portal
- Huawei: OAuth connection via FusionSolar
- Sungrow: OAuth connection via iSolarCloud
- SMA: API key from Sunny Portal
- Solis: API key from SolisCloud
- Fronius: API key from Fronius Solar.web
- GoodWe: API key from SEMS Portal
- Fox ESS, Solax, and others: Additional OEMs supported

### How to connect an integration
- Go to Settings → Integrations
- Find the manufacturer you want to connect
- For API key integrations (SolarEdge, SMA, Solis, Fronius, GoodWe): Enter the API key from the manufacturer portal and click Connect
- For OAuth integrations (Huawei, Sungrow): Click Connect, which redirects you to the manufacturer login page. Authorise Metris and you will be redirected back
${callout('note','API key vs OAuth','Some manufacturers use simple API keys that you copy and paste. Others (Huawei, Sungrow) use OAuth, meaning you log into their portal to grant Metris access. OAuth connections may need periodic re-authorisation.')}
### Integration statuses
StatusMeaningActionConnectedActive and pulling dataNone requiredPausedAuthentication expired or failedRe-authenticate the integrationInactiveNot connectedComplete setup
### Linking sites to integrations

After connecting an OEM at the organisation level, you need to link individual sites. Go to a site's assets page and select the connected integration. Metris will list the available devices (inverters or meters) from the manufacturer portal, and you map them to the site.

### What data is collected
- Inverter integrations: Generation data (kWh), device status, fault codes, and serial numbers
- Meter integrations: Consumption, export, import, and self-consumption data

Data is collected every 15 to 60 minutes depending on the manufacturer, and integration status is polled every 5 minutes to detect connection issues.
${callout('tip','Tip','Connect your integration at the organisation level first, then link sites individually. This way one set of credentials covers all sites using the same manufacturer.')}
### Troubleshooting connections

Paused status: Re-authenticate via Settings → Integrations. OAuth tokens expire and need renewal.

Missing devices: Ensure the devices are visible in the manufacturer portal and that the API account has access to them.

Partial data: Some manufacturers rate-limit API calls. Data will backfill as subsequent calls succeed.
${callout('action','Recommended Action','After connecting a new integration, allow 24 hours for data to populate. Check the site overview to confirm data is flowing for each device.')}

---

## Article 19: Accounting integrations: Xero & SunSystems

### Supported accounting systems

Metris integrates with two accounting platforms to automatically sync invoices:
- Xero: Cloud-based accounting (OAuth connection)
- SunSystems: Enterprise accounting system

### Connecting Xero
- Go to Settings → Integrations
- Click Connect next to Xero
- You will be redirected to Xero to authorise access
- Select the Xero tenant (organisation) to link
- Configure the account code and tax type for invoice line items

Once connected, every invoice you generate in Metris is automatically created in Xero with the correct account coding.
${callout('note','Note','Xero OAuth tokens expire periodically. If the integration shows Paused, re-authenticate from the Integrations settings page. No data is lost during a pause. Invoices sync once the connection is restored.')}
### Connecting SunSystems

SunSystems integration works through an automated export. Invoices created in Metris are pushed to SunSystems with a unique reference ID. The SunSystems invoice ID is shown alongside the Metris invoice number on each invoice detail page.

### What gets synced

For both integrations, the following data is pushed to your accounting system:
- Invoice number, date, and due date
- Customer details and billing address
- Line items with quantities (kWh), unit prices, and totals
- Tax amounts and rates
- SPV (Special Purpose Vehicle) details where applicable

### Italian XML invoices

For Italian operations, Metris supports XML invoice export compliant with Italian e-invoicing regulations (FatturaPA). When this is enabled for your organisation:
- Invoice consolidation is automatically disabled (each invoice must be individual)
- Tax items can be added manually to each invoice
- XML export is available per invoice cycle
${callout('tip','Tip','If an invoice fails to sync, you will see an error indicator on the invoice. Use the Retry button to re-attempt the sync without having to recreate the invoice.')}
### Failed sync handling

If an invoice fails to create in Xero or SunSystems, Metris flags the invoice with an integration error. You can:
- Check the error message for details
- Fix any issues (e.g. missing account codes, expired connection)
- Click Retry to re-attempt the sync
${callout('action','Recommended Action','After connecting Xero, create a test invoice to verify account codes and tax types are mapped correctly before running a full invoice cycle.')}

---

## Article 20: How invoice cycles work

### What is an invoice cycle?

An invoice cycle is a billing period you define by selecting a start date, end date, and the sites to include. Metris then calculates the energy consumed or exported during that period and generates invoices for each customer.

### Creating an invoice cycle
- Go to Invoices → Create Invoice Cycle
- Set the billing period (start and end dates)
- Select the sites to include
- Click Generate Preview

### The preview step

Before any invoices are created, Metris runs a dry run showing you:
- Each customer who will receive an invoice
- The site(s) included
- kWh consumed or exported during the period
- The total amount based on configured rates

You can review every invoice and deselect any you do not want to generate.
${callout('tip','Tip','Always review the preview before generating. If kWh figures look unexpected, check the site data for that period before proceeding.')}
### Invoice consolidation

For customers with multiple sites, you can consolidate into a single invoice rather than sending separate invoices per site. This is enabled by default but is automatically disabled for Italian XML invoicing.

### After generation

Once generated, each invoice appears in draft status. From here you can:
- Edit individual line items, add miscellaneous charges, or adjust quantities
- Send the invoice to the customer via email
- Export a PDF of the invoice
- Sync to your accounting system (Xero or SunSystems)

### How energy charges are calculated
Energy Charge = kWh Consumed × Rate per kWh (p/kWh)
The kWh value comes from meter or inverter data for the billing period. The rate comes from the pricing configuration on the site (see Article 21).

### Invoice statuses
StatusMeaningDraftGenerated but not yet sentSentEmailed to customerViewedCustomer has opened the invoicePartialPartially paidOverduePast due date and unpaidPaidFully paid${callout('action','Recommended Action','Set up a regular cadence for invoice cycles. Most asset managers run monthly cycles in the first week of the following month once meter data has been received.')}

---

## Article 21: Pricing structures and tariff configuration

### How pricing works

Every site in Metris has a price configuration that determines how energy charges are calculated on invoices. The price is the rate per kWh that the customer pays for consumed or exported energy.

### Setting prices manually
- Navigate to the site's Agreements page
- Click Add Price
- Enter the price value (p/kWh or £/kWh), the price type, and the date it takes effect

Prices are date-based. When a new price is added with a commencement date, it applies from that date forward. Previous prices remain for historical billing.

### Using pricing templates

For portfolios with consistent pricing across multiple sites, you can create pricing templates:
- Go to Pricing Templates
- Create a template with the standard rates
- Apply the template to sites during setup or via the site agreements page
${callout('tip','Tip','Pricing templates save time when onboarding multiple sites with the same PPA terms. You can always override template prices on individual sites.')}
### Price types

The price type determines which energy flow is billed:
- Consumption rate: Applied to energy consumed on-site
- Export rate: Applied to energy exported to the grid
- Generation rate: Applied to total generation (common for FiT sites)

### How prices flow to invoices

When you create an invoice cycle, Metris automatically looks up the active price for each site during the billing period and multiplies it by the relevant kWh figure:
Invoice Amount = kWh × Active Price (p/kWh) for the billing period
If a price changed mid-billing period, the system applies the correct rate to the days before and after the change.
${callout('note','Note','If a site has no price configured, the invoice preview will show £0.00 for that site. Always verify pricing is set before running an invoice cycle.')}
### PPA commitments

For sites under Power Purchase Agreements, Metris tracks:
- Self-consumption percentage commitment: The percentage of generation the customer commits to consume on-site
- Self-consumption absolute commitment: A fixed kWh commitment

These are tracked on the site's PPA details and may affect billing terms.
${callout('action','Recommended Action','Review pricing for all sites before generating your first invoice cycle. Missing or incorrect prices are the most common cause of unexpected invoice amounts.')}

---

## Article 22: Payments and Stripe integration

### Payment options

Metris supports online payments through Stripe, giving your customers a straightforward way to pay invoices:
- One-off payments: Customer clicks a payment link on their invoice and pays via card
- Direct debit: Customer sets up a recurring mandate for automatic payments

### Setting up Stripe
- Go to Settings → Integrations
- Click Connect next to Stripe
- Follow the Stripe onboarding flow to link your bank account
- Once connected, payment options become available on invoices
${callout('note','Note','Stripe must be enabled for your organisation. If you do not see the Stripe option in Integrations, contact your account manager to enable the payments module.')}
### How one-off payments work
- You generate and send an invoice to a customer
- The customer views their invoice in the Customer Portal
- They click Pay Invoice, which opens a Stripe checkout page
- After payment, the invoice status automatically updates to Paid

### Direct debit setup

Customers can set up direct debit mandates from the Customer Portal:
- On their site overview, they will see a prompt to set up direct debit
- Clicking the setup link creates a Stripe mandate
- Once the mandate is active, future invoices are charged automatically

### Direct debit statuses
StatusMeaningPendingMandate submitted, waiting for bank confirmationActiveMandate confirmed, payments will be collectedExpiredMandate no longer valid, needs re-setup
### Tracking payments

All payments are recorded in Metris with:
- The payment amount and date
- The Stripe payment ID for reconciliation
- The payment method (card or direct debit)
- The associated invoice

Payments also sync to your connected accounting system (Xero or SunSystems) for automatic reconciliation.
${callout('action','Recommended Action','Enable Stripe and encourage customers to set up direct debit. Automated collection reduces overdue invoices and manual reconciliation effort.')}

---

## Article 23: Customer Portal overview

### What is the Customer Portal?

The Customer Portal is a dedicated platform for your end customers. It gives the businesses consuming or exporting solar energy visibility into their energy data, invoices, and environmental impact without needing access to the full management platform.

### Customer Portal sections

After logging in, customers land on their Sites page showing all sites they have access to. Each site has three main tabs:

### Overview
- Site card: Address, location map, PPA type, asset manager name, and next invoice cycle
- Energy consumption chart: Self-consumption vs grid consumption over time
- Energy generation chart: Generation vs export over time
- Key metrics: Energy generated this month, invoice count with status badges

Charts support date range filtering and can be grouped by day, week, or month. Metris automatically converts units between kWh and MWh based on scale.

### Billing & Usage
- Full invoice history with status indicators (New, Overdue, Paid)
- Invoice details including energy breakdown, charges, tax, and notes
- PDF download for each invoice
- Consumption chart showing usage during the billing period
- Payment button (if Stripe is enabled)
- Direct debit setup and management

### Insights
- CO₂ prevented: Total carbon emissions avoided (kg CO₂e)
- Equivalent oak trees: A tangible representation of carbon savings
- Self-consumption percentage: How much solar energy is used on-site
- Carbon savings chart: CO₂ savings vs emissions over time
${callout('note','Generation-only mode','For sites without consumption data, the Customer Portal automatically simplifies the view. Consumption charts and the Insights tab are hidden, showing only generation and export data.')}
### Customer settings

Customers can manage their own profile from the avatar menu:
- Edit name
- Change password
- View email (read-only)
${callout('tip','Tip','The Customer Portal is designed to answer the questions customers ask most: "How much energy am I using?", "What am I paying?", and "What is my environmental impact?" without needing to contact you.')}
### Branding

The Customer Portal displays your organisation or SPV logo in the header. This is configured at the organisation level and gives customers a branded experience.
${callout('action','Recommended Action','Walk through the Customer Portal yourself before inviting customers. Understanding what they see helps you anticipate questions and set expectations.')}

---

## Article 24: How carbon impact is calculated

### Why carbon impact matters

The Customer Portal shows your customers how much carbon dioxide their solar installation is preventing. This data supports corporate sustainability reporting, ESG compliance, and environmental value reporting to stakeholders.

### The core calculation

Carbon savings are calculated by multiplying the energy generated by a grid emissions factor:
CO₂ Savings = Energy Generation (kWh) × 0.207074 (kg CO₂/kWh)
The default factor of 0.207074 kg CO₂ per kWh represents the average carbon intensity of the UK electricity grid, sourced from the UK Government GHG Conversion Factors published by the Department for Energy Security and Net Zero (DESNZ). Every kWh of solar generation displaces this amount of fossil-fuel-generated electricity.
${callout('note','Emission factor','The 0.207074 kg CO₂/kWh factor is sourced from the UK Government GHG Conversion Factors, updated annually. Metris reviews and applies the latest factor as part of our annual platform update cycle. The factor is also configurable per site for non-UK installations where grid carbon intensity differs.')}
### Embodied carbon

Metris also accounts for the carbon cost of manufacturing and installing the solar system itself:
Embodied Emissions = Installed Capacity (kW) × 800 (kg CO₂/kW)
The default embodied emissions factor is 800 kg CO₂ per kW of installed capacity. This represents the approximate lifecycle carbon cost of panel manufacturing, transport, and installation.

### Net carbon reduction
Net CO₂ Reduction = CO₂ Savings − Embodied Emissions
Over time, cumulative CO₂ savings far exceed the one-time embodied emissions, showing the long-term environmental benefit of the installation.

### What customers see

On the Insights tab, customers see three key metrics:
MetricWhat it showsCO₂ preventedTotal kg CO₂e avoided for the selected periodEquivalent oak treesNumber of mature oak trees that would absorb the same amount of CO₂Self-consumption %Percentage of solar generation consumed on-site
### Carbon savings chart

The Insights page also shows a time-series chart with:
- Green bars: CO₂ savings per period (energy generated × emission factor)
- Dark bars: CO₂ emissions per period (embodied carbon amortised)

This gives customers a clear visual of their ongoing environmental impact.
${callout('tip','Tip','The oak tree equivalent is a useful metric for customer communications and sustainability reports. One mature oak tree absorbs approximately 22 kg of CO₂ per year.')}
### Date range filtering

Customers can filter their carbon data by preset ranges:
- Year to date (YTD)
- Month to date (MTD)
- Quarter to date (QTD)
- Last month, last 30/60/90 days
${callout('action','Recommended Action','Ensure each site has the correct installed capacity configured. This directly affects the embodied emissions calculation and the accuracy of the net carbon reduction figure.')}

---

## Article 25: Customer onboarding and access

### Customer vs user accounts

Metris has two types of accounts:
- Users access the Manage Platform (asset managers and O&M providers)
- Contacts access the Customer Portal (end customers)

Contacts are created under Customer organisations and linked to specific sites.

### Inviting a customer
- Go to Customers and select the customer organisation
- Click Add Contact
- Enter the contact's name, email, and billing email
- Assign access to specific sites
- Save. The contact receives an onboarding email with a link to set up their password

### Customer onboarding flow

When a customer clicks the onboarding link in their email:
- They land on the Account Setup page
- They create a password (with confirmation)
- They are automatically logged in and redirected to their sites
${callout('note','Note','The onboarding link contains a unique token tied to the contact email. It is a one-time use link. If the customer needs a new link, you can resend the invitation.')}
### Managing customer access

Each contact can be given access to one or more sites. They will only see data for the sites they are assigned to. You can:
- Add or remove site access at any time
- Update their contact details and billing email
- Tag contacts for filtering and organisation

### Customer profile details

For each contact, Metris stores:
- Name, email, and billing email
- Address and billing address
- Tags for categorisation
- Associated customer organisation

### Password management

Customers can reset their own password via the Forgot Password flow on the login page. They can also change their password from the Settings menu once logged in.
${callout('tip','Tip','Add a billing email if invoices should go to a finance team rather than the main contact. Metris uses the billing email for invoice delivery when set.')}
### What happens when a customer logs in

The Customer Portal is fully separate from the Manage Platform. Customers cannot see other customers, portfolio-level data, or any management features. They see only their assigned sites with energy, billing, and insights data.
${callout('action','Recommended Action','Before inviting a customer, ensure their sites have data flowing and at least one invoice cycle has been generated. This gives them a meaningful first experience.')}

---

## Article 26: Using the O&M ticket system

### What tickets are for

The O&M (Operations & Maintenance) ticket system lets you track maintenance tasks, fault resolution, and scheduled work. Tickets can be linked to alerts so you have a complete audit trail from issue detection to resolution.

### Creating a ticket
- Go to O&M from the main navigation
- Click Create Ticket
- Fill in the required fields: title, site, priority, and description
- Optionally assign to an O&M provider user and set a scheduled date
- Optionally link to an existing alert
${callout('tip','Tip','You can also create a ticket directly from the Alerts table. Click "Create Ticket" next to any alert and the ticket will be pre-populated with the alert context.')}
### Ticket priorities
PriorityWhen to useCriticalComplete system failure or major safety issueHighSignificant revenue loss or multi-inverter failureMediumSingle device failure or performance degradationLowMinor issue or scheduled maintenanceNo PriorityInformational or tracking only
### Ticket workflow

Tickets move through these statuses:
- Assigned: Ticket created and assigned to a user
- Scheduled: A date has been set for the work
- In Review: Work completed, awaiting confirmation
- Flagged: Issue requires further attention or escalation
- Done: Ticket resolved and closed

### Working with tickets

Each ticket has a detail view where you can:
- Add activities: Comments and updates as work progresses
- Attach files: Photos, documents, or reports related to the issue
- Change status: Move the ticket through the workflow
- Update assignee: Reassign to a different O&M user
- View linked alert: Jump to the original alert that triggered the ticket

### Alert-to-ticket flow

The recommended workflow for handling alerts is:
- Alert appears in the Alerts table
- Verify the alert is genuine (not a brief data glitch)
- Create an O&M ticket from the alert
- The O&M provider investigates and updates the ticket
- Once resolved, the ticket is marked Done
- The alert resolves automatically when the issue clears
${callout('action','Recommended Action','Create tickets for any alert lasting more than 24 hours. This ensures every issue has an owner and a resolution trail for reporting purposes.')}

---

## Article 27: Managing O&M providers

### What O&M providers are

O&M (Operations & Maintenance) providers are external contractors or internal teams responsible for maintaining your solar sites. In Metris, they have their own user accounts with access scoped to the sites they manage.

### Provider vs standard users

Provider users differ from standard users in several ways:
- They belong to a Provider organisation, not your asset management organisation
- They can only see sites they are explicitly assigned to
- They cannot access billing, invoicing, or financial data
- They can view alerts, manage tickets, and update ticket status for their assigned sites

### Adding a provider
- Go to Settings → Providers
- Create a new Provider organisation with the company details
- Add individual provider users with their name and email
- Assign the provider to specific sites

### Assigning providers to sites

Each site can have one O&M provider assigned. When a provider is linked to a site:
- Their users appear in the ticket assignee dropdown for that site
- They can view the site's alerts and asset status
- They can be assigned tickets and update ticket progress
${callout('note','Note','A provider user can be assigned to multiple sites. When creating a ticket, the assignee dropdown only shows provider users who have access to the selected site.')}
### Provider access and permissions

Provider users have a focused view of the platform designed for maintenance operations:
- Can access: Site overview, equipment status, alerts, and O&M tickets
- Cannot access: Financial data, invoices, customer details, or organisation settings

### Coordinating with providers

The ticket system is designed to be the primary coordination channel between asset managers and O&M providers:
- Asset manager creates a ticket and assigns it to a provider user
- Provider receives the ticket with full context (alert details, site info)
- Provider updates the ticket with progress, photos, and notes
- Asset manager reviews and closes the ticket when satisfied
${callout('tip','Tip','Encourage your O&M providers to add activities and attach photos to tickets. This creates a maintenance audit trail useful for investor reporting and contract compliance.')}
### Multiple providers

You can have different O&M providers for different sites. This is common when your portfolio spans multiple regions or when different contractors specialise in different equipment types.
${callout('action','Recommended Action','Set up your O&M providers before the first alert arrives. Having the provider structure in place means you can create and assign tickets immediately when issues occur.')}

---

## Article 17: Formula reference sheet

### Performance metrics
AvailabilityTime with energy output ÷ (Total test time − Excluded downtime)Standard PRActual Generation ÷ Expected Generation (SolarGIS)Ideal PRActual Generation ÷ (GTI × Array Capacity)Technical PRAny PR method, all intervals, no exclusionsContractual PRAny PR method with exclusion periods removed
### Energy calculations
Irradiance-based generationGTI × Capacity × Target PRWeighted irradianceΣ(GTI × Array Capacity) ÷ Total CapacityExportGeneration − ConsumptionSelf-consumptionGeneration − Export
### Carbon calculations
CO₂ savingsGeneration (kWh) × 0.207074 (kg CO₂/kWh)Embodied emissionsInstalled Capacity (kW) × 800 (kg CO₂/kW)Net carbon reductionCO₂ Savings − Embodied Emissions
### Revenue calculations
FiT total valueGeneration Tariff + Export Tariff + Self-Consumption SavingsGeneration tariff revenueTotal Generation (kWh) × FiT Rate (p/kWh)Export tariff revenueExport (kWh) × FiT Export Rate (p/kWh)Self-consumption savingsSelf-Consumption (kWh) × Avoided Import Rate (p/kWh)
### Billing calculations
Energy chargekWh Consumed × Rate per kWh (p/kWh)Tax amountTaxable Amount × (Tax Rate ÷ 100)Invoice totalSubtotal + Tax − Discount