# GraphQL Schema Design — {Domain Name}

> Relay-compliant | Version {0.1} | {Date} | Status: {Draft/Review/Approved}

## 1. Schema Overview

| Field | Value |
|-------|-------|
| Schema scope | {e.g. User management, Order processing} |
| Federation | {Standalone / Subgraph of federated gateway} |
| Auth mechanism | {e.g. JWT via `Authorization` header} |

## 2. Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Types | PascalCase | `UserProfile` |
| Fields | camelCase | `firstName` |
| Enums | PascalCase type, SCREAMING_SNAKE_CASE values | `enum Status { ACTIVE }` |
| Input types | `{Verb}{Type}Input` | `CreateUserInput` |
| Payloads | `{Verb}{Type}Payload` | `CreateUserPayload` |
| Connections | `{Type}Connection` | `UserConnection` |

## 3. Type Definitions

```graphql
type User implements Node {
  id: ID!              # Global Relay ID
  email: String!       # Required at creation
  displayName: String  # Nullable — optional
  role: UserRole!      # Defaults to MEMBER
  createdAt: DateTime!
}
enum UserRole { ADMIN MEMBER VIEWER }
```

{Add types. Document nullability rationale per field.}

## 4. Query Type

```graphql
type Query {
  node(id: ID!): Node
  user(id: ID!): User
  users(first: Int, after: String, filter: UserFilter): UserConnection!
}
input UserFilter { role: UserRole, search: String }
```

## 5. Mutation Type

```graphql
type Mutation { createUser(input: CreateUserInput!): CreateUserPayload! }
input CreateUserInput { email: String!, displayName: String, role: UserRole }
type CreateUserPayload { user: User, userErrors: [UserError!]! }
type UserError { field: [String!]!, message: String!, code: UserErrorCode! }
enum UserErrorCode { INVALID_EMAIL DUPLICATE_EMAIL FORBIDDEN }
```

{Repeat pattern for update/delete mutations.}

## 6. Subscription Type

```graphql
type Subscription { userUpdated(userId: ID!): User! }
```

{Remove this section if subscriptions are not needed.}

## 7. Connections / Pagination (Relay Spec)

```graphql
type UserConnection { edges: [UserEdge!]!, pageInfo: PageInfo!, totalCount: Int! }
type UserEdge { cursor: String!, node: User! }
type PageInfo { hasNextPage: Boolean!, hasPreviousPage: Boolean!, startCursor: String, endCursor: String }
```

All list queries must use cursor-based connections.

## 8. Error Handling

Mutation payloads include `userErrors` for domain errors. Transport errors use the standard GraphQL `errors` array. Example domain error: `{"data":{"createUser":{"user":null,"userErrors":[{"field":["email"],"message":"Already taken","code":"DUPLICATE_EMAIL"}]}}}`.

## 9. N+1 Prevention

| Strategy | Details |
|----------|---------|
| DataLoader | Batch and cache DB lookups per request |
| Query complexity | Max: {500}; reject queries exceeding limit |
| Depth limit | Max depth: {10} |

## 10. Schema Evolution

| Rule | Details |
|------|---------|
| Additive only | New fields and types may be added freely |
| No removals | `@deprecated(reason: "...")` for {6 months} before removal |
| Non-null promotion | A nullable field must never become non-null |
| Changelog | Record every schema change in the API changelog |
