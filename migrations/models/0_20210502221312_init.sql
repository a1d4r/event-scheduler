-- upgrade --
CREATE TABLE IF NOT EXISTS "event" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "start" TIMESTAMPTZ NOT NULL,
    "end" TIMESTAMPTZ NOT NULL,
    "duration" BIGINT NOT NULL
);
COMMENT ON TABLE "event" IS 'Event for which we are looking the most suitable time.';
CREATE TABLE IF NOT EXISTS "timetable" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "participant_name" VARCHAR(100) NOT NULL,
    "event_id" INT NOT NULL REFERENCES "event" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "timetable" IS 'Participant name and all time intervals which are suitable for him/her.';
CREATE TABLE IF NOT EXISTS "timeinterval" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start" TIMESTAMPTZ NOT NULL,
    "end" TIMESTAMPTZ NOT NULL,
    "timetable_id" INT NOT NULL REFERENCES "timetable" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "timeinterval" IS 'Single time interval which is suitable for a participant.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
