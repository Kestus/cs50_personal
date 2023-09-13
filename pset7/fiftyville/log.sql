-- Keep a log of any SQL queries you execute as you solve the mystery.

-- airports                  crime_scene_reports       people
-- atm_transactions          flights                   phone_calls
-- bank_accounts             interviews
-- courthouse_security_logs  passengers

-- Find out what crime took place on July 28, 2020 on Chamberlin Street.
SELECT *
FROM crime_scene_reports
WHERE year=2020 AND month=7 AND day=28 AND street LIKE "Chamberlin Street";
-- Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
-- Interviews were conducted today with three witnesses who were present at the time —
-- each of their interview transcripts mentions the courthouse.
-- ID 295

-- Check interviews corresponding to that day, containing word "courthouse" in the transcript.
SELECT *
FROM interviews
WHERE year=2020 AND month=7 AND day=28 AND transcript LIKE "%courthouse%";
-- Ruth - Sometime within ten minutes of the theft, I saw the thief get into a car in the
--  courthouse parking lot and drive away. If you have security footage from the courthouse parking lot,
--  you might want to look for cars that left the parking lot in that time frame.
-- Eugene - I don't know the thief's name, but it was someone I recognized.
--  Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street
--  and saw the thief there withdrawing some money.
-- Raymond - As the thief was leaving the courthouse, they called someone who talked to them
--  for less than a minute. In the call, I heard the thief say that they were planning to take the earliest
--  flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the
--  phone to purchase the flight ticket.

-- Check courthouse security logs.
SELECT license_plate
FROM courthouse_security_logs
WHERE year=2020 AND month=7 AND day=28 AND hour=10 AND minute>15 AND minute<25;
-- To many cars left courthouse at that timeframe to determine.
-- Plates:
-- 5P2BI95
-- 94KL13X
-- 6P58WS2
-- 4328GD8
-- G412CB7
-- L93JTIZ
-- 322W7JE
-- 0NTHK55

-- Check ATM on Fifer Street.
SELECT account_number FROM atm_transactions WHERE year=2020 AND month=7 AND day=28 AND atm_location="Fifer Street" AND transaction_type="withdraw";
-- Account numbers:
-- 28500762
-- 28296815
-- 76054385
-- 49610011
-- 16153065
-- 25506511
-- 81061156
-- 26013199

-- From people and bank_accounts find person, that have both account number and license plate,
--  spotted at corresponding time and place.
SELECT *
FROM people JOIN bank_accounts ON people.id=bank_accounts.person_id
WHERE people.license_plate IN
(
SELECT license_plate
FROM courthouse_security_logs
WHERE year=2020 AND month=7 AND day=28 AND hour=10 AND minute>15 AND minute<25
)
AND bank_accounts.account_number IN
(
SELECT account_number
FROM atm_transactions
WHERE year=2020 AND month=7 AND day=28 AND atm_location="Fifer Street" AND transaction_type="withdraw"
);
-- id | name | phone_number | passport_number | license_plate | account_number | person_id | creation_year
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X | 49610011 | 686048 | 2010
-- 514354 | Russell | (770) 555-1861 | 3592750733 | 322W7JE | 26013199 | 514354 | 2012
-- 396669 | Elizabeth | (829) 555-5269 | 7049073643 | L93JTIZ | 25506511 | 396669 | 2014
-- 467400 | Danielle | (389) 555-5198 | 8496433585 | 4328GD8 | 28500762 | 467400 | 2014

-- Now find who, out of these people, made a phone call, duration of whitch was less than 60 seconds.
SELECT *
FROM phone_calls
WHERE year=2020 AND month=7 AND day=28 AND duration<60
AND caller IN
(
SELECT phone_number
FROM people JOIN bank_accounts ON people.id=bank_accounts.person_id
WHERE people.license_plate IN
(
SELECT license_plate
FROM courthouse_security_logs
WHERE year=2020 AND month=7 AND day=28 AND hour=10 AND minute>15 AND minute<25
)
AND bank_accounts.account_number IN
(
SELECT account_number
FROM atm_transactions
WHERE year=2020 AND month=7 AND day=28 AND atm_location="Fifer Street" AND transaction_type="withdraw"
));
-- id | caller | receiver | year | month | day | duration
-- 233 | (367) 555-5533 | (375) 555-8161 | 2020 | 7 | 28 | 45
-- 255 | (770) 555-1861 | (725) 555-3243 | 2020 | 7 | 28 | 49

-- id | name | phone_number | passport_number | license_plate | account_number | person_id | creation_year
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X | 49610011 | 686048 | 2010
-- OR
-- 514354 | Russell | (770) 555-1861 | 3592750733 | 322W7JE | 26013199 | 514354 | 2012

-- What airport is in Fiftyville?
SELECT * FROM airports WHERE city LIKE "Fiftyville";
-- id | abbreviation | full_name | city
-- 8 | CSF | Fiftyville Regional Airport | Fiftyville

-- Who got on the plane the next day, from Fiftyville airport.
SELECT *
FROM flights JOIN passengers ON flights.id=passengers.flight_id
WHERE flights.origin_airport_id=8
AND flights.year=2020 AND flights.month=7 AND flights.day=29
AND passengers.passport_number IN (5773159633, 3592750733)
ORDER BY hour
;
-- id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | flight_id | passport_number | seat
-- 36 | 8 | 4 | 2020 | 7 | 29 | 8 | 20 | 36 | 5773159633 | 4A
-- 18 | 8 | 6 | 2020 | 7 | 29 | 16 | 0 | 18 | 3592750733 | 4C
-- Ernest 5773159633 took earliest flight out of the Fiftyville, next day after theft.

-- Where did he escape?
-- Check whitch city the airport with id "4" is in.
SELECT city FROM airports WHERE id=4;
-- London

-- Who is accomplice?
-- To whom number, Ernest called at the day of theft, belongs. ((375) 555-8161)
SELECT name FROM people WHERE phone_number LIKE "(375) 555-8161";
-- Berthold