import http from "k6/http";
import { check, sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";

// ---------------------------------------------------------------------------
// Custom metrics — track domain-specific measurements beyond k6 built-ins
// ---------------------------------------------------------------------------
const errorRate = new Rate("custom_error_rate");
const requestCount = new Counter("custom_request_count");
const latency = new Trend("custom_latency", true); // true = time values

// ---------------------------------------------------------------------------
// Options — define load scenarios and pass/fail thresholds
// ---------------------------------------------------------------------------
export const options = {
  scenarios: {
    // Smoke: verify the system works with minimal load
    smoke: {
      executor: "ramping-vus",
      startVUs: 1,
      stages: [{ duration: "30s", target: 3 }],
      tags: { test_type: "smoke" },
    },
    // Average: simulate normal production traffic
    average: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "1m", target: 20 },   // ramp up
        { duration: "3m", target: 20 },   // hold steady
        { duration: "1m", target: 0 },    // ramp down
      ],
      startTime: "1m",
      tags: { test_type: "average" },
    },
    // Stress: push beyond normal to find the breaking point
    stress: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "2m", target: 50 },
        { duration: "3m", target: 50 },
        { duration: "1m", target: 0 },
      ],
      startTime: "6m",
      tags: { test_type: "stress" },
    },
    // Spike: sudden burst of traffic
    spike: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "10s", target: 100 },
        { duration: "30s", target: 100 },
        { duration: "10s", target: 0 },
      ],
      startTime: "12m",
      tags: { test_type: "spike" },
    },
  },

  // Thresholds — if any of these fail, the test exits with a non-zero code
  thresholds: {
    http_req_duration: ["p(95)<500", "p(99)<1500"],   // 95th percentile < 500ms
    http_req_failed: ["rate<0.01"],                    // less than 1% failures
    custom_error_rate: ["rate<0.05"],                  // custom: less than 5%
  },
};

// ---------------------------------------------------------------------------
// Setup — runs once before all VUs. Use for auth tokens, seed data, etc.
// ---------------------------------------------------------------------------
export function setup() {
  const BASE_URL = __ENV.BASE_URL || "http://localhost:3000";
  // Example: obtain an auth token
  // const loginRes = http.post(`${BASE_URL}/api/auth/login`, JSON.stringify({
  //   username: __ENV.TEST_USER,
  //   password: __ENV.TEST_PASS,
  // }), { headers: { "Content-Type": "application/json" } });
  // return { token: loginRes.json("token"), baseUrl: BASE_URL };

  return { baseUrl: BASE_URL };
}

// ---------------------------------------------------------------------------
// Default function — runs once per VU iteration
// ---------------------------------------------------------------------------
export default function (data) {
  const res = http.get(`${data.baseUrl}/api/health`, {
    tags: { endpoint: "health" },
    // headers: { Authorization: `Bearer ${data.token}` },
  });

  // Record custom metrics
  requestCount.add(1);
  latency.add(res.timings.duration);

  // Validate response
  const passed = check(res, {
    "status is 200": (r) => r.status === 200,
    "response time < 500ms": (r) => r.timings.duration < 500,
  });

  errorRate.add(!passed);

  // Simulate user think-time between requests
  sleep(Math.random() * 3 + 1); // 1-4 seconds
}

// ---------------------------------------------------------------------------
// Teardown — runs once after all VUs finish. Use for cleanup.
// ---------------------------------------------------------------------------
export function teardown(data) {
  // Example: delete test data created during setup
  // http.del(`${data.baseUrl}/api/test-data`);
}
