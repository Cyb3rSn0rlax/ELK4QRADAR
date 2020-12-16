SELECT  "Offense_Id" as 'OffenseID',
RULENAME("Rule_ID") AS 'RuleName',
DATEFORMAT(starttime,'yyyy-MM-dd hh:mm:ss a') AS StartTime,
DATEFORMAT(endtime,'yyyy-MM-dd hh:mm:ss a') AS StorageTime,
DATEFORMAT(devicetime,'yyyy-MM-dd hh:mm:ss a') AS LogSourceTime,
QIDNAME(qid) AS 'EventName'
FROM events
WHERE qid='28250369'
LAST 24 HOURS