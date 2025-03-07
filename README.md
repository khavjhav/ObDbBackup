```
Create Function Details:

1. Select a Template:
   - Choose a template for your function from the available options.

2. Template Details:
   - Additional information is required to create the function. Please provide the necessary details.

3. Job Type:
   - Select the job type. For example, "Create new app."

4. Schedule:
   - Enter a CRON expression to specify the schedule for the function.
   - The CRON expression format is: `{second} {minute} {hour} {day} {month} {day of week}`.

Example CRON Expressions:
   - Every 5 minutes: `0 */5 * * * *`
   - Daily at 3:00 AM UTC: `0 0 3 * * *`

Error:
   - If you see the error `[x] Invalid Cron Expression`, it means the provided CRON expression is not valid.
   - Please consult the official Azure documentation for guidance on creating valid CRON expressions:
     [Azure Timer Trigger Documentation](https://azure.microsoft.com/en-us/documentation/articles/functions-bindings-timer/)

Note:
   - Ensure that the CRON expression matches the required format and is appropriate for your scheduling needs.
```
