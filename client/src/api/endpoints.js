const BASE_URL = "http://localhost:8000";

const AUTH_URLS = {
  AUTH: "/auth",
  REFRESH: "/auth/token/refresh",
  CHECK: "/auth/check",
};

const PATIENTS_URLS = {
  PATIENT: "/patient",
  ALL: "/patient/all",
};

const RECORDS_URLS = {
  RECORD: "/record",
  ALL: "/record/all",
};

const RUBRICS_URLS = {
  RUBRIC: "/rubric",
  SECTION: "/rubric/section",
  ALL: "/rubric/all",
};

export { BASE_URL, AUTH_URLS, PATIENTS_URLS, RECORDS_URLS, RUBRICS_URLS };
