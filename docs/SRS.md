# Software Requirements Specification (SRS)

## CrowdFund — Crowdfunding Platform

| Field          | Value                             |
|----------------|-----------------------------------|
| Document ID    | SRS-CF-001                        |
| Version        | 1.0                               |
| Date           | 2025-11-25                        |
| Status         | Final                             |
| Prepared by    | CrowdFund Engineering Team        |
| Standard       | IEEE Std 830-1998                 |

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [Purpose](#11-purpose)
   - 1.2 [Scope](#12-scope)
   - 1.3 [Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
   - 1.4 [Overview](#14-overview)
2. [Overall Description](#2-overall-description)
   - 2.1 [Product Perspective](#21-product-perspective)
   - 2.2 [Product Functions](#22-product-functions)
   - 2.3 [User Classes and Characteristics](#23-user-classes-and-characteristics)
   - 2.4 [Operating Environment](#24-operating-environment)
   - 2.5 [Design Constraints](#25-design-constraints)
   - 2.6 [Assumptions and Dependencies](#26-assumptions-and-dependencies)
3. [System Architecture](#3-system-architecture)
   - 3.1 [Architectural Overview](#31-architectural-overview)
   - 3.2 [Component Diagram](#32-component-diagram)
4. [Functional Requirements](#4-functional-requirements)
   - 4.1 [Authentication and User Accounts](#41-authentication-and-user-accounts)
   - 4.2 [Campaign Creation and Management](#42-campaign-creation-and-management)
   - 4.3 [Campaign Browsing and Search](#43-campaign-browsing-and-search)
   - 4.4 [Donation Processing](#44-donation-processing)
   - 4.5 [Donation History and Receipts](#45-donation-history-and-receipts)
   - 4.6 [Admin Moderation](#46-admin-moderation)
   - 4.7 [Campaign Updates](#47-campaign-updates)
5. [Non-Functional Requirements](#5-non-functional-requirements)
   - 5.1 [Performance](#51-performance)
   - 5.2 [Security](#52-security)
   - 5.3 [Usability](#53-usability)
   - 5.4 [Reliability](#54-reliability)
   - 5.5 [Scalability](#55-scalability)
   - 5.6 [Maintainability](#56-maintainability)
6. [External Interface Requirements](#6-external-interface-requirements)
   - 6.1 [User Interface](#61-user-interface)
   - 6.2 [Software Interfaces](#62-software-interfaces)
   - 6.3 [Communication Interfaces](#63-communication-interfaces)
7. [Data Requirements](#7-data-requirements)
   - 7.1 [Entity Descriptions](#71-entity-descriptions)
   - 7.2 [Conceptual ER Diagram](#72-conceptual-er-diagram)
8. [Use Cases](#8-use-cases)
   - 8.1 [UC-01: Browse Campaigns](#81-uc-01-browse-campaigns)
   - 8.2 [UC-02: Create Campaign](#82-uc-02-create-campaign)
   - 8.3 [UC-03: Donate to Campaign](#83-uc-03-donate-to-campaign)
   - 8.4 [UC-04: Admin Moderation](#84-uc-04-admin-moderation)
9. [System Diagrams](#9-system-diagrams)
   - 9.1 [Use Case Diagram](#91-use-case-diagram)
   - 9.2 [Sequence Diagram — Donation Process](#92-sequence-diagram--donation-process)
   - 9.3 [ER Diagram](#93-er-diagram)
10. [Future Enhancements](#10-future-enhancements)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document describes the functional and non-functional requirements for the **CrowdFund** web-based crowdfunding platform. The document is intended for:

- Software developers and architects implementing the system
- Quality assurance engineers writing and executing test cases
- Project managers and stakeholders tracking scope and acceptance criteria
- System administrators responsible for deployment and operations

The SRS defines what the system must do, the constraints it must operate under, and the qualities it must exhibit. It does not prescribe detailed design or implementation decisions.

### 1.2 Scope

**CrowdFund** is a web-based crowdfunding platform that enables individuals and organizations to raise money for projects, causes, or creative endeavours. The platform connects three primary actors — *Visitors*, *Donors*, and *Campaign Organizers* — under the supervision of *Administrators*.

Key capabilities of the software product:

- User registration and authentication with role-based access
- Campaign creation, editing, and lifecycle management by organizers
- Public discovery and search of active fundraising campaigns
- Secure donation processing and payment handling
- Real-time progress tracking (goal vs. amount raised)
- Email confirmations and PDF receipts for donors
- Administrative tools for campaign and user moderation
- AI-powered chatbot assistant for platform guidance (RAG-based)

The product is delivered as a single-page web application (frontend) backed by a REST API (backend) and a relational database. Mobile-native applications are out of scope for version 1.0.

### 1.3 Definitions, Acronyms, and Abbreviations

| Term / Acronym | Definition |
|----------------|------------|
| **SRS** | Software Requirements Specification |
| **Campaign** | A fundraising initiative created by an organizer with a monetary goal and a deadline |
| **Donor** | A registered or guest user who contributes money to a campaign |
| **Organizer / Creator** | A registered user who creates and manages campaigns |
| **Admin** | A privileged user who moderates platform content and users |
| **Visitor** | An unauthenticated user browsing the platform |
| **Goal Amount** | The target monetary amount an organizer wishes to raise |
| **Raised Amount** | The total money donated to a campaign to date |
| **JWT** | JSON Web Token — used for stateless authentication |
| **API** | Application Programming Interface |
| **REST** | Representational State Transfer |
| **HTTPS** | HyperText Transfer Protocol Secure |
| **ORM** | Object-Relational Mapper |
| **RAG** | Retrieval-Augmented Generation — the AI chatbot subsystem |
| **SPA** | Single-Page Application |
| **UI** | User Interface |
| **CORS** | Cross-Origin Resource Sharing |
| **GDPR** | General Data Protection Regulation |
| **PCI-DSS** | Payment Card Industry Data Security Standard |

### 1.4 Overview

The remainder of this document is organised as follows:

- **Section 2** provides an overall description of the product, its context, user classes, and constraints.
- **Section 3** describes the system architecture and component relationships.
- **Section 4** specifies the functional requirements using "The system shall…" statements.
- **Section 5** details non-functional quality requirements.
- **Section 6** describes external interface requirements.
- **Section 7** defines the data model and conceptual ER diagram.
- **Section 8** provides detailed use cases.
- **Section 9** presents system diagrams (use case, sequence, and ER).
- **Section 10** outlines planned future enhancements.

---

## 2. Overall Description

### 2.1 Product Perspective

CrowdFund is a new, self-contained web application. It does not replace an existing system but complements the broader ecosystem of crowdfunding solutions by offering an open, extensible platform. The system interfaces with:

- **External Payment Gateway** (e.g., Stripe) for processing card and digital wallet transactions.
- **Email Delivery Service** (e.g., SendGrid / SMTP) for transactional emails (registration confirmations, donation receipts, campaign updates).
- **Cloud Image Storage** (e.g., Cloudinary) for campaign cover images and user profile pictures.
- **OpenAI API** for the optional RAG-based AI assistant.

The system is intended to operate as a cloud-hosted service with a PostgreSQL database backend and a React-based SPA frontend served via a CDN or web server.

### 2.2 Product Functions

The major functions of the system are summarised below:

| # | Function | Description |
|---|----------|-------------|
| F1 | User Registration & Login | Create accounts, authenticate, manage profiles |
| F2 | Campaign Lifecycle | Create, update, publish, and close campaigns |
| F3 | Campaign Discovery | Browse, search, filter, and categorise campaigns |
| F4 | Donation Processing | Securely accept and record monetary donations |
| F5 | Progress Tracking | Display real-time goal vs. raised amounts |
| F6 | Receipts & History | Provide donors with email confirmations and history |
| F7 | Admin Moderation | Review, approve, suspend, or remove campaigns/users |
| F8 | Comments & Follows | Allow donors to comment and follow campaigns |
| F9 | Campaign Updates | Let organizers post updates to backers |
| F10 | AI Chatbot | Answer user questions about the platform via RAG |

### 2.3 User Classes and Characteristics

**2.3.1 Visitor (Unauthenticated User)**

- General public browsing the site without an account
- Can view campaign listings and individual campaign pages
- Can search and filter campaigns
- Cannot donate, create campaigns, or post comments
- Minimal technical expertise assumed

**2.3.2 Donor (Registered User — Donor Role)**

- Registered and authenticated platform user
- Primary motivation: support campaigns they believe in
- Can make donations, view their donation history, post comments, and follow campaigns
- May receive email receipts and campaign update notifications
- General level of technical proficiency; comfortable with online payments

**2.3.3 Organizer / Campaign Creator (Registered User — Creator Role)**

- Registered and authenticated platform user with the creator role
- Creates, manages, and publishes fundraising campaigns
- Can post campaign updates, respond to comments, and view analytics dashboards
- Moderate level of digital literacy; expected to write compelling campaign descriptions

**2.3.4 Administrator**

- Internal staff member with elevated platform privileges
- Responsible for approving new campaigns, handling abuse reports, managing users, and maintaining platform health
- High technical proficiency; accesses dedicated admin interface

**2.3.5 AI Chatbot (System Actor)**

- Automated subsystem responding to natural-language queries
- Not a human user class but modelled as an actor in use case diagrams where relevant

### 2.4 Operating Environment

| Layer | Technology / Constraint |
|-------|-------------------------|
| Client browser | Chrome ≥ 110, Firefox ≥ 110, Safari ≥ 16, Edge ≥ 110 |
| Frontend runtime | React 18+, Vite, Tailwind CSS, ShadCN UI |
| Backend runtime | Python 3.10+, Flask 3.x, Flask-RESTX |
| Database | PostgreSQL 14+ |
| ORM / Migrations | SQLAlchemy, Flask-Migrate (Alembic) |
| Authentication | JWT (PyJWT), bcrypt password hashing |
| Hosting | Cloud provider (AWS, GCP, Railway, or equivalent) |
| Reverse proxy | NGINX or cloud load balancer with TLS termination |
| WSGI server | Gunicorn (production), Flask dev server (development only) |
| Image storage | Cloudinary (external) |
| Email service | SMTP-compatible or SendGrid API |
| Payment | Stripe API (external) |

### 2.5 Design Constraints

1. **IEEE 830 Compliance** — this document follows the IEEE 830-1998 SRS standard.
2. **PCI-DSS** — card data must never be stored on CrowdFund servers; all payment processing is delegated to the payment gateway.
3. **GDPR / Data Privacy** — users must be able to request deletion of their personal data. Personal data must be encrypted at rest and in transit.
4. **Stateless API** — the backend REST API must be stateless; session state is maintained on the client via JWT tokens.
5. **Responsive Design** — the frontend must render correctly on desktop (≥ 1024 px) and tablet (768 – 1023 px) viewports.
6. **Open Source Stack** — core framework components must be open-source to avoid vendor lock-in.

### 2.6 Assumptions and Dependencies

1. A valid Stripe account with API keys is available prior to processing live payments.
2. A Cloudinary account is configured for image uploads.
3. An email delivery service (SMTP or SendGrid) is available for transactional emails.
4. Users have a stable internet connection; offline functionality is not required.
5. The PostgreSQL database server is provisioned and accessible to the backend application.
6. The OpenAI API key is available if the RAG chatbot feature is enabled.
7. Campaign organizers are responsible for the legality and accuracy of their campaign content.
8. The platform will initially support **English** language only; i18n scaffolding may be added later.

---

## 3. System Architecture

### 3.1 Architectural Overview

CrowdFund employs a **three-tier client-server architecture**:

| Tier | Component | Responsibility |
|------|-----------|----------------|
| Presentation | React SPA (frontend) | Render UI, handle routing, call REST API |
| Application | Flask REST API (backend) | Business logic, auth, data validation, orchestration |
| Data | PostgreSQL database | Persistent storage of all application entities |

Additional cross-cutting concerns:

- **Authentication** is handled via JWT tokens issued by the backend; the frontend stores the token in memory / localStorage and attaches it as a Bearer header on authenticated requests.
- **Payment processing** is handled entirely by the external payment gateway (Stripe); the backend only stores transaction references and statuses.
- **Image storage** is delegated to Cloudinary; the frontend uploads images directly to Cloudinary and stores the resulting URL in the database via the API.
- **Email delivery** is triggered by backend events (registration, donation, campaign updates) and sent via an SMTP service or the SendGrid API.
- **AI Chatbot** (RAG) is an optional subsystem running alongside the backend, using a local Chroma vector store and the OpenAI LLM for question answering.

### 3.2 Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER BROWSER                                   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │              React SPA (Frontend)                                │  │
│  │  Pages: Home | Campaigns | Campaign Detail | Login | Register    │  │
│  │  Creator Dashboard | Donor Dashboard | Admin Panel | Chat UI     │  │
│  └────────────────────┬─────────────────────────────────────────────┘  │
└───────────────────────│─────────────────────────────────────────────────┘
                        │  HTTPS / REST (JSON)
                        ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                       BACKEND API (Flask / Gunicorn)                      │
│                                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │  Auth Routes │  │ Campaign     │  │ Donation     │  │ Admin       │  │
│  │  /users      │  │ Routes       │  │ Routes       │  │ Routes      │  │
│  │  /auth       │  │ /campaigns   │  │ /donations   │  │ /admin      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘  │
│         │                 │                  │                  │         │
│  ┌──────┴─────────────────┴──────────────────┴──────────────────┴──────┐ │
│  │              SQLAlchemy ORM + Business Logic Layer                  │ │
│  └──────────────────────────────────┬────────────────────────────────┘  │
│                                     │                                    │
│  ┌──────────────────────────────┐   │   ┌─────────────────────────────┐ │
│  │  RAG Chatbot (Optional)      │   │   │  Email Service (SMTP /      │ │
│  │  LangChain + Chroma +        │   │   │  SendGrid)                  │ │
│  │  OpenAI Embeddings / LLM     │   │   └─────────────────────────────┘ │
│  └──────────────────────────────┘   │                                    │
└─────────────────────────────────────│────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────────────┐
│   PostgreSQL DB     │  │  Payment Gateway    │  │  Cloud Image Store   │
│   (SQLAlchemy)      │  │  (Stripe API)       │  │  (Cloudinary)        │
│                     │  │                     │  │                      │
│  Users, Campaigns,  │  │  Card processing,   │  │  Campaign images,    │
│  Donations,         │  │  Webhooks,          │  │  Profile pictures    │
│  Comments, etc.     │  │  Refunds            │  │                      │
└─────────────────────┘  └─────────────────────┘  └──────────────────────┘
```

---

## 4. Functional Requirements

Requirements are numbered **FR-X.Y** where X identifies the feature group and Y is the individual requirement.

### 4.1 Authentication and User Accounts

**FR-1.1** The system shall allow any visitor to register for a new account by providing a unique username, a valid email address, a password, and a chosen role (Donor or Organizer).

**FR-1.2** The system shall hash all passwords using bcrypt with a minimum work factor of 12 before storing them in the database.

**FR-1.3** The system shall issue a signed JWT access token upon successful authentication; the token shall expire after 24 hours.

**FR-1.4** The system shall allow registered users to log in using their email address and password.

**FR-1.5** The system shall return a descriptive error message when login credentials are invalid, without revealing which field (email or password) is incorrect.

**FR-1.6** The system shall allow authenticated users to view and update their profile information (username, profile picture, biography).

**FR-1.7** The system shall allow users to change their password after verifying their current password.

**FR-1.8** The system shall allow administrators to deactivate or ban user accounts.

**FR-1.9** The system shall prevent deactivated or banned users from logging in and shall return an appropriate HTTP 403 response.

**FR-1.10** The system shall support password reset via a time-limited (≤ 1 hour) email link.

### 4.2 Campaign Creation and Management

**FR-2.1** The system shall allow users with the Organizer role to create a new campaign by providing a title, description, category, goal amount, start date, end date, and at least one cover image.

**FR-2.2** The system shall validate that the campaign end date is at least 24 hours after the start date.

**FR-2.3** The system shall validate that the campaign goal amount is a positive number greater than zero.

**FR-2.4** The system shall set a newly created campaign to *Pending* status, awaiting administrator review before becoming publicly visible.

**FR-2.5** The system shall allow organizers to edit campaign details (title, description, image, goal, dates) while the campaign is in *Pending* or *Active* status.

**FR-2.6** The system shall automatically transition a campaign to *Completed* status when its end date passes or when the raised amount equals or exceeds the goal amount.

**FR-2.7** The system shall allow organizers to voluntarily close (cancel) an active campaign, setting its status to *Cancelled*.

**FR-2.8** The system shall allow organizers to delete campaigns that are in *Pending* or *Cancelled* status and have zero donations.

**FR-2.9** The system shall display the organizer dashboard showing a list of their campaigns with status indicators, raised amounts, donor counts, and progress percentages.

**FR-2.10** The system shall track and store the total `raised_amount` for each campaign, updating it atomically with each confirmed donation.

### 4.3 Campaign Browsing and Search

**FR-3.1** The system shall display a publicly accessible campaign listing page showing all *Active* campaigns, ordered by creation date (newest first) by default.

**FR-3.2** The system shall allow any visitor to search campaigns by keyword matching against campaign title and description.

**FR-3.3** The system shall allow visitors to filter campaigns by category, status, and minimum/maximum goal amount.

**FR-3.4** The system shall allow visitors to sort campaigns by: newest, most funded (highest raised amount), most popular (highest donor count), and ending soon (earliest end date).

**FR-3.5** The system shall display paginated results with a configurable page size (default: 12 campaigns per page).

**FR-3.6** The system shall display a campaign detail page showing: title, description, organizer name, category, cover image, goal amount, raised amount, progress percentage, number of donors, start/end dates, and status.

**FR-3.7** The system shall display a visual progress bar on the campaign detail page reflecting the ratio of raised amount to goal amount.

**FR-3.8** The system shall allow authenticated users to follow a campaign and receive notifications for updates posted by the organizer.

**FR-3.9** The system shall allow authenticated users to post, edit, and delete their own comments on campaign pages.

### 4.4 Donation Processing

**FR-4.1** The system shall allow authenticated Donor users to initiate a donation to any *Active* campaign.

**FR-4.2** The system shall present a donation form requesting: donation amount (minimum $1.00), and payment method details routed securely through the payment gateway.

**FR-4.3** The system shall validate that the donation amount is a positive number and meets the minimum threshold before submitting to the payment gateway.

**FR-4.4** The system shall create a *Donation* record with status *Pending* when a donation is initiated.

**FR-4.5** The system shall confirm the donation and update its status to *Completed* only after receiving a successful payment confirmation from the payment gateway.

**FR-4.6** The system shall increment the campaign's `raised_amount` by the confirmed donation amount atomically (inside a database transaction) upon successful payment confirmation.

**FR-4.7** The system shall update the donation status to *Failed* if the payment gateway returns a failure response, and shall not alter the campaign's raised amount.

**FR-4.8** The system shall not store raw card numbers or CVV codes; all sensitive payment data shall be handled exclusively by the payment gateway (tokenisation).

**FR-4.9** The system shall support donations made by anonymous donors (where the donor chooses not to display their name publicly).

### 4.5 Donation History and Receipts

**FR-5.1** The system shall allow authenticated users to view a complete history of their past donations, including campaign name, donation amount, date, and payment status.

**FR-5.2** The system shall send an email confirmation to the donor within 60 seconds of a successful donation, containing: campaign title, donation amount, transaction reference, and date.

**FR-5.3** The system shall provide a downloadable PDF receipt for each completed donation, accessible from the donor's donation history page.

**FR-5.4** The system shall allow campaign organizers to view a list of donors for their campaigns (donor name, amount, date) unless the donor has opted for anonymity.

**FR-5.5** The system shall display aggregate donation statistics on the campaign detail page (total raised, number of donors, average donation amount).

### 4.6 Admin Moderation

**FR-6.1** The system shall provide an administrator-only dashboard listing all campaigns awaiting approval (*Pending* status).

**FR-6.2** The system shall allow administrators to approve a *Pending* campaign, transitioning it to *Active* status and making it publicly visible.

**FR-6.3** The system shall allow administrators to reject a *Pending* campaign with a mandatory rejection reason that is communicated to the organizer via email.

**FR-6.4** The system shall allow administrators to suspend an *Active* campaign (e.g., due to policy violation), hiding it from public listings.

**FR-6.5** The system shall allow administrators to reactivate a *Suspended* campaign after a policy violation is resolved.

**FR-6.6** The system shall allow administrators to permanently delete campaigns and associated data.

**FR-6.7** The system shall allow administrators to view, search, and manage all registered user accounts.

**FR-6.8** The system shall allow administrators to ban user accounts, preventing login and public activity.

**FR-6.9** The system shall record all administrative actions in an immutable `AdminLogs` table, capturing: admin user ID, action type, target entity type, target entity ID, and timestamp.

**FR-6.10** The system shall allow administrators to view and delete abusive or spam comments reported by users.

### 4.7 Campaign Updates

**FR-7.1** The system shall allow campaign organizers to post text-based updates on their campaigns at any time while the campaign is *Active* or *Completed*.

**FR-7.2** The system shall display campaign updates chronologically on the campaign detail page (newest first).

**FR-7.3** The system shall notify all followers of a campaign via email when a new update is posted.

**FR-7.4** The system shall allow organizers to edit or delete their own campaign updates.

**FR-7.5** The system shall associate each update with a timestamp and the organizer's identity.

---

## 5. Non-Functional Requirements

### 5.1 Performance

**NFR-1.1** The system shall return campaign listing API responses within **500 ms** at the 95th percentile under a load of 200 concurrent users.

**NFR-1.2** The system shall process and confirm a donation payment within **3 seconds** from submission to payment gateway confirmation under normal load.

**NFR-1.3** The system shall load the initial campaign listing page (first meaningful paint) within **2 seconds** on a standard broadband connection (≥ 10 Mbps).

**NFR-1.4** Database queries for campaign search and filtering shall be executed within **200 ms** by leveraging appropriate indexes on frequently queried columns (`title`, `category`, `status`, `end_date`).

### 5.2 Security

**NFR-2.1** All communications between the client browser and the server shall be encrypted using TLS 1.2 or higher (HTTPS).

**NFR-2.2** The system shall implement JWT token expiry and shall reject expired or tampered tokens with HTTP 401.

**NFR-2.3** The system shall enforce role-based access control (RBAC) on all API endpoints; unauthenticated or unauthorised requests shall receive HTTP 401 or HTTP 403 respectively.

**NFR-2.4** The system shall protect all state-changing endpoints against Cross-Site Request Forgery (CSRF) by requiring the JWT Bearer token (not cookies alone).

**NFR-2.5** The system shall validate and sanitise all user-supplied input on the server side to prevent SQL injection, XSS, and other injection attacks.

**NFR-2.6** Sensitive configuration values (database credentials, API keys, JWT secret) shall be stored as environment variables and shall never be committed to version control.

**NFR-2.7** The system shall comply with PCI-DSS requirements by delegating all card data handling to the certified payment gateway.

**NFR-2.8** The system shall implement rate limiting of **100 requests per minute per IP** on authentication endpoints to mitigate brute-force attacks.

**NFR-2.9** Passwords must meet a minimum complexity requirement: at least 8 characters, containing at least one uppercase letter, one lowercase letter, and one digit.

### 5.3 Usability

**NFR-3.1** The application shall be fully functional on the latest two major versions of Chrome, Firefox, Safari, and Edge.

**NFR-3.2** The user interface shall be responsive and usable on screen widths from 768 px (tablet) upward.

**NFR-3.3** All form validation errors shall be displayed inline adjacent to the relevant field within 200 ms of user interaction.

**NFR-3.4** The donation flow shall be completable in no more than **4 steps** from the campaign page.

**NFR-3.5** The system shall display progress indicators (loading spinners) for operations that take longer than 300 ms.

**NFR-3.6** The platform shall achieve a minimum Web Content Accessibility Guidelines (WCAG) 2.1 Level AA conformance rating.

### 5.4 Reliability

**NFR-4.1** The system shall achieve **99.5% uptime** (measured monthly), excluding scheduled maintenance windows.

**NFR-4.2** The system shall implement database transactions for all multi-step financial operations to ensure atomicity; partial updates shall be rolled back on failure.

**NFR-4.3** Automated daily database backups shall be maintained with a minimum retention period of 30 days.

**NFR-4.4** The system shall implement graceful error handling; unhandled exceptions shall return structured JSON error responses and shall be logged to an error-tracking service without exposing stack traces to the client.

**NFR-4.5** The payment gateway integration shall implement idempotency keys to prevent duplicate charges in the event of network retries.

### 5.5 Scalability

**NFR-5.1** The backend application shall be stateless so that multiple instances can be deployed behind a load balancer without session affinity.

**NFR-5.2** The system architecture shall support horizontal scaling of the backend tier by adding additional application server instances.

**NFR-5.3** Database read scalability shall be achievable through the addition of read replicas without changes to the application code.

**NFR-5.4** Static frontend assets shall be served from a CDN to reduce origin server load and improve global latency.

**NFR-5.5** The system shall handle up to **1,000 concurrent users** without degradation in response times exceeding the thresholds defined in Section 5.1.

### 5.6 Maintainability

**NFR-6.1** The backend codebase shall maintain a minimum test coverage of **70%** on business-logic modules.

**NFR-6.2** All database schema changes shall be managed via versioned Alembic migration scripts; manual DDL changes to the production database are prohibited.

**NFR-6.3** The REST API shall be documented using the OpenAPI 3.0 specification, auto-generated via Flask-RESTX, and accessible at `/api/docs`.

**NFR-6.4** The system shall use structured logging (JSON format) to facilitate integration with log aggregation tools (e.g., CloudWatch, ELK stack).

**NFR-6.5** The frontend shall be organised into reusable components; no component shall exceed 300 lines of code.

---

## 6. External Interface Requirements

### 6.1 User Interface

**EI-1.1** The frontend shall be implemented as a React SPA with client-side routing, providing seamless navigation without full page reloads.

**EI-1.2** The UI shall use Tailwind CSS and ShadCN UI component library to ensure consistent visual design and accessibility primitives.

**EI-1.3** Navigation shall include a persistent top navigation bar with: platform logo, campaign search bar, login/register links (unauthenticated), and user profile menu (authenticated).

**EI-1.4** Campaign cards on listing pages shall display: cover image, title, organizer name, category badge, progress bar, raised amount, goal amount, and days remaining.

**EI-1.5** The donation modal/page shall include a clear summary of the campaign being donated to, an amount input, and a Stripe-hosted payment element for card details.

**EI-1.6** The admin panel shall be accessible only to users with the Administrator role and shall provide tabbed views for Campaigns, Users, and Logs management.

### 6.2 Software Interfaces

**EI-2.1 Payment Gateway (Stripe)**

| Attribute | Detail |
|-----------|--------|
| Interface type | REST API over HTTPS |
| SDK | `stripe-python` (backend), Stripe.js / Stripe Elements (frontend) |
| Key operations | Create Payment Intent, Confirm Payment, Retrieve Payment, Refund |
| Event notifications | Stripe Webhooks (`payment_intent.succeeded`, `payment_intent.payment_failed`) |
| Authentication | Stripe secret key (backend), publishable key (frontend) |

**EI-2.2 Email Delivery Service (SMTP / SendGrid)**

| Attribute | Detail |
|-----------|--------|
| Interface type | SMTP protocol or SendGrid REST API |
| Trigger events | User registration, donation confirmation, password reset, campaign updates, moderation decisions |
| Email format | HTML + plain-text multipart MIME |
| Personalisation | Transactional templates with dynamic variables (username, amount, campaign title) |

**EI-2.3 Cloud Image Storage (Cloudinary)**

| Attribute | Detail |
|-----------|--------|
| Interface type | Cloudinary Upload API (HTTPS) |
| Upload flow | Frontend uploads image directly to Cloudinary; resulting `secure_url` stored in database via backend |
| Transformations | On-the-fly resizing, format conversion (WebP), cropping |
| Security | Signed upload presets to prevent unauthorized uploads |

**EI-2.4 OpenAI API (RAG Chatbot — Optional)**

| Attribute | Detail |
|-----------|--------|
| Interface type | OpenAI REST API over HTTPS |
| Models used | `text-embedding-ada-002` (embeddings), `gpt-4o-mini` or equivalent (LLM) |
| Data flow | User query → LangChain retriever → Chroma vector search → OpenAI LLM → structured answer |

### 6.3 Communication Interfaces

**EI-3.1** All client-to-server communication shall use **HTTPS (TLS 1.2+)** on port 443.

**EI-3.2** The REST API shall use **JSON** as its data exchange format; all responses shall include a `Content-Type: application/json` header.

**EI-3.3** Authentication shall use the **HTTP Authorization header** with the `Bearer <token>` scheme.

**EI-3.4** Stripe payment events shall be received via **HTTPS Webhooks**; the backend shall verify the webhook signature using the Stripe webhook signing secret before processing.

**EI-3.5** The system shall support **CORS** with configurable allowed origins; in production, only the registered frontend domain(s) shall be whitelisted.

**EI-3.6** Long-running operations (e.g., export generation) may use **HTTP Server-Sent Events (SSE)** or polling to communicate progress to the frontend.

---

## 7. Data Requirements

### 7.1 Entity Descriptions

#### 7.1.1 User

Represents a registered platform user.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `user_id` | Integer | PK, Auto-increment | Unique identifier |
| `username` | VARCHAR(80) | NOT NULL, UNIQUE | Public display name |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE | Login email address |
| `password_hash` | VARCHAR(128) | NOT NULL | bcrypt hash of password |
| `role` | ENUM | NOT NULL | `donor`, `organizer`, `admin` |
| `profile_image` | TEXT | NULLABLE | Cloudinary URL of profile picture |
| `bio` | TEXT | NULLABLE | Short user biography |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account activation flag |
| `is_banned` | BOOLEAN | DEFAULT FALSE | Admin ban flag |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Registration timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last update timestamp |

#### 7.1.2 Campaign

Represents a fundraising campaign.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `campaign_id` | Integer | PK, Auto-increment | Unique identifier |
| `creator_id` | Integer | FK → User.user_id, NOT NULL | Campaign organizer |
| `title` | VARCHAR(200) | NOT NULL | Campaign title |
| `description` | TEXT | NOT NULL | Full campaign description |
| `category` | ENUM | NOT NULL | E.g., `technology`, `arts`, `health`, `education`, `community` |
| `goal_amount` | DECIMAL(12,2) | NOT NULL, > 0 | Fundraising goal in USD |
| `raised_amount` | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total donations received |
| `start_date` | DATE | NOT NULL | Campaign launch date |
| `end_date` | DATE | NOT NULL | Campaign deadline |
| `image` | TEXT | NULLABLE | Cover image Cloudinary URL |
| `status` | ENUM | NOT NULL, DEFAULT `pending` | `pending`, `active`, `completed`, `cancelled`, `suspended` |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last update timestamp |

#### 7.1.3 Donation

Records an individual donation transaction.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `donation_id` | Integer | PK, Auto-increment | Unique identifier |
| `donor_id` | Integer | FK → User.user_id, NOT NULL | Donating user |
| `campaign_id` | Integer | FK → Campaign.campaign_id, NOT NULL | Target campaign |
| `amount` | DECIMAL(12,2) | NOT NULL, > 0 | Donation amount in USD |
| `status` | ENUM | NOT NULL, DEFAULT `pending` | `pending`, `completed`, `failed`, `refunded` |
| `is_anonymous` | BOOLEAN | DEFAULT FALSE | Hide donor identity publicly |
| `payment_reference` | VARCHAR(255) | NULLABLE, UNIQUE | Gateway transaction ID |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Donation initiation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last status update timestamp |

#### 7.1.4 CampaignUpdate

Stores updates posted by campaign organizers.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `update_id` | Integer | PK, Auto-increment | Unique identifier |
| `campaign_id` | Integer | FK → Campaign.campaign_id, NOT NULL | Associated campaign |
| `author_id` | Integer | FK → User.user_id, NOT NULL | Organizer who posted the update |
| `title` | VARCHAR(200) | NOT NULL | Update headline |
| `content` | TEXT | NOT NULL | Update body text |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Post timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last edit timestamp |

#### 7.1.5 AdminLogs

Immutable audit trail of administrative actions.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `log_id` | Integer | PK, Auto-increment | Unique identifier |
| `admin_id` | Integer | FK → User.user_id, NOT NULL | Admin who performed the action |
| `action_type` | VARCHAR(100) | NOT NULL | E.g., `approve_campaign`, `ban_user`, `delete_comment` |
| `entity_type` | VARCHAR(50) | NOT NULL | E.g., `campaign`, `user`, `comment` |
| `entity_id` | Integer | NOT NULL | ID of the affected entity |
| `notes` | TEXT | NULLABLE | Optional freeform notes or reason |
| `performed_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Action timestamp |

#### 7.1.6 Additional Entities (Supporting)

- **Comment** — user comments on campaigns (comment_id, user_id, campaign_id, content, likes, created_at)
- **UserFollows** — junction table for user–campaign follow relationships (user_id, campaign_id, followed_at)
- **Payment** — payment gateway metadata linked to a donation (payment_id, donation_id, gateway_response, created_at)
- **ChatHistory** — RAG chatbot conversation history (chat_id, user_id, role, message, timestamp)

### 7.2 Conceptual ER Diagram

```
┌──────────────────┐         ┌──────────────────────┐
│      User        │         │       Campaign        │
│──────────────────│         │──────────────────────│
│ PK user_id       │────┐    │ PK campaign_id        │
│    username      │    │    │ FK creator_id ────────┤
│    email         │    │    │    title              │
│    password_hash │    │    │    description        │
│    role          │    │    │    category           │
│    profile_image │    │    │    goal_amount        │
│    is_active     │    │    │    raised_amount      │
│    is_banned     │    │    │    start_date         │
│    created_at    │    │    │    end_date           │
└──────────────────┘    │    │    image              │
         │               │    │    status             │
         │ 1             │    └──────────────────────┘
         │               │              │ 1
    ┌────┴───────┐        │         ┌───┴────────────┐
    │  Donation  │        │         │ CampaignUpdate │
    │────────────│        │         │────────────────│
    │ PK don_id  │        │         │ PK update_id   │
    │ FK donor_id│────────┘         │ FK campaign_id │
    │ FK camp_id │                  │ FK author_id   │
    │    amount  │                  │    title        │
    │    status  │                  │    content      │
    │    is_anon │                  │    created_at   │
    │    pay_ref │                  └────────────────┘
    └────────────┘
         │ 1
         │
    ┌────┴───────┐
    │  Payment   │
    │────────────│
    │ PK pay_id  │
    │ FK don_id  │
    │  gateway   │
    │  response  │
    │ created_at │
    └────────────┘

┌──────────────────┐         ┌──────────────────┐
│    AdminLogs     │         │    Comment        │
│──────────────────│         │──────────────────│
│ PK log_id        │         │ PK comment_id     │
│ FK admin_id      │         │ FK user_id        │
│    action_type   │         │ FK campaign_id    │
│    entity_type   │         │    content        │
│    entity_id     │         │    likes          │
│    notes         │         │    created_at     │
│    performed_at  │         └──────────────────┘
└──────────────────┘

┌──────────────────┐         ┌──────────────────┐
│   UserFollows    │         │   ChatHistory    │
│──────────────────│         │──────────────────│
│ FK user_id       │         │ PK chat_id        │
│ FK campaign_id   │         │ FK user_id        │
│    followed_at   │         │    role           │
└──────────────────┘         │    message        │
                             │    timestamp      │
                             └──────────────────┘
```

---

## 8. Use Cases

### 8.1 UC-01: Browse Campaigns

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-01 |
| **Name** | Browse Campaigns |
| **Actors** | Visitor, Donor, Organizer (any unauthenticated or authenticated user) |
| **Description** | A user views and filters the list of active campaigns to find one of interest |

**Preconditions:**
- The platform is accessible via a web browser
- At least one campaign exists in *Active* status

**Main Flow:**
1. The user navigates to the campaign listing page (e.g., `/campaigns`)
2. The system retrieves and displays the first page of *Active* campaigns ordered by creation date (newest first)
3. Each campaign card shows: cover image, title, progress bar, raised amount, goal amount, category badge, and days remaining
4. The user optionally enters a keyword in the search bar
5. The system filters and returns campaigns matching the keyword in title or description
6. The user optionally selects a category filter from the dropdown
7. The system refines results to the selected category
8. The user optionally selects a sort order (e.g., "Ending Soon")
9. The system re-orders results accordingly
10. The user clicks on a campaign card
11. The system navigates to the campaign detail page (UC-03 may follow)

**Alternative Flow A — No Matching Campaigns:**
- At step 5: If no campaigns match the search keyword, the system displays a "No campaigns found" message with a suggestion to broaden the search

**Alternative Flow B — Pagination:**
- At step 10: The user clicks the "Next Page" button; the system loads and displays the next batch of campaigns

**Postconditions:**
- The user has viewed the campaign listing
- No data was modified
- The system logged the page view (anonymously) for analytics purposes

---

### 8.2 UC-02: Create Campaign

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-02 |
| **Name** | Create Campaign |
| **Actors** | Organizer, Administrator |
| **Description** | An authenticated organizer creates a new fundraising campaign and submits it for admin review |

**Preconditions:**
- The actor is authenticated with the Organizer role
- The actor has a valid session (JWT token)

**Main Flow:**
1. The organizer navigates to the "Create Campaign" page
2. The system displays a campaign creation form
3. The organizer enters: title, description, category, goal amount, start date, end date
4. The organizer uploads a cover image via the image uploader
5. The system uploads the image to Cloudinary and stores the URL
6. The organizer clicks "Submit Campaign"
7. The system validates all required fields and business rules (e.g., end date > start date, goal > 0)
8. The system creates the campaign record with status *Pending*
9. The system sends an email notification to the organizer confirming submission
10. The system notifies administrators of the new pending campaign
11. An administrator reviews the campaign in the admin panel
12. The administrator approves the campaign, transitioning it to *Active*
13. The system emails the organizer that their campaign is now live

**Alternative Flow A — Validation Failure:**
- At step 7: If validation fails, the system highlights the invalid fields with error messages and does not submit the form

**Alternative Flow B — Admin Rejects Campaign:**
- At step 12: The administrator clicks "Reject" and enters a rejection reason
- The system transitions the campaign to *Rejected* status
- The system emails the organizer with the rejection reason

**Postconditions:**
- A new Campaign record exists in the database
- The campaign is in *Active* status (approved) or *Pending*/*Rejected* status (if awaiting/rejected)
- The admin action is recorded in AdminLogs

---

### 8.3 UC-03: Donate to Campaign

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-03 |
| **Name** | Donate to Campaign |
| **Actors** | Donor, Payment Gateway (Stripe), Email Service |
| **Description** | An authenticated donor makes a monetary contribution to an active campaign |

**Preconditions:**
- The donor is authenticated and has the Donor role
- The target campaign is in *Active* status
- The payment gateway is operational

**Main Flow:**
1. The donor views the campaign detail page
2. The donor clicks the "Donate" button
3. The system displays the donation modal with the campaign title and an amount input
4. The donor enters a donation amount (≥ $1.00) and optionally selects anonymous donation
5. The donor clicks "Proceed to Payment"
6. The system creates a Payment Intent via the Stripe API and displays the Stripe payment element
7. The donor enters their card details in the Stripe-hosted payment element
8. The donor clicks "Confirm Donation"
9. Stripe processes the payment and returns a success event
10. The system receives the Stripe webhook `payment_intent.succeeded`
11. The system creates/updates the Donation record with status *Completed*
12. The system increments the campaign's `raised_amount` atomically
13. The system sends a donation confirmation email to the donor with a receipt
14. The campaign detail page updates the progress bar to reflect the new raised amount

**Alternative Flow A — Payment Declined:**
- At step 9: Stripe returns a payment failure
- The system updates the Donation record to *Failed*
- The system displays an error message to the donor
- The campaign's raised amount is not changed

**Alternative Flow B — Network Timeout:**
- At step 10: The webhook does not arrive within the expected window
- The system's scheduled reconciliation job queries the Stripe API for the Payment Intent status
- If confirmed, the system proceeds from step 11

**Alternative Flow C — Campaign Reaches Goal During Donation:**
- At step 12: After incrementing raised_amount, the system checks if raised_amount ≥ goal_amount
- If so, the system transitions the campaign status to *Completed*
- The system notifies the organizer that their goal has been reached

**Postconditions:**
- A completed Donation record exists in the database
- The campaign's `raised_amount` has been incremented
- The donor has received an email confirmation
- The donor can view the donation in their history

---

### 8.4 UC-04: Admin Moderation

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-04 |
| **Name** | Admin Moderation |
| **Actors** | Administrator |
| **Description** | An administrator reviews, approves, rejects, or suspends a campaign or manages user accounts |

**Preconditions:**
- The actor is authenticated with the Administrator role

**Main Flow (Campaign Moderation):**
1. The administrator navigates to the admin panel
2. The system displays a list of *Pending* campaigns awaiting review
3. The administrator selects a campaign to review
4. The system displays the full campaign details
5. The administrator clicks "Approve"
6. The system transitions the campaign to *Active* and records the action in AdminLogs
7. The system emails the organizer that the campaign is approved and live

**Alternative Flow A — Reject Campaign:**
- At step 5: The administrator clicks "Reject" and enters a mandatory rejection reason
- The system transitions the campaign to *Rejected*
- AdminLogs records the rejection action and reason
- The system emails the organizer with the rejection reason

**Alternative Flow B — Suspend Active Campaign:**
1. The administrator searches for a campaign by title or ID
2. The administrator selects an *Active* campaign
3. The administrator clicks "Suspend" and provides a reason
4. The system transitions the campaign to *Suspended*, hiding it from public listings
5. AdminLogs records the suspension
6. The organizer is notified by email

**Alternative Flow C — Ban User:**
1. The administrator navigates to the Users section
2. The administrator searches for a user
3. The administrator clicks "Ban User" and provides a reason
4. The system sets `is_banned = true` on the user record
5. AdminLogs records the ban action
6. Any active JWT tokens for the user are invalidated on the next request

**Postconditions:**
- The target entity (campaign or user) is updated to its new state
- An immutable record exists in AdminLogs for the action
- Relevant parties are notified via email

---

## 9. System Diagrams

### 9.1 Use Case Diagram

```
                     ┌──────────────────────────────────────────────────┐
                     │              CrowdFund Platform                  │
                     │                                                  │
                     │  ┌─────────────────┐   ┌──────────────────────┐ │
  ┌───────────┐      │  │  Browse         │   │  Register / Login    │ │
  │  Visitor  │──────┼─►│  Campaigns      │   │                      │ │
  └───────────┘      │  └─────────────────┘   └──────────────────────┘ │
        │            │                                                  │
        │            │  ┌─────────────────┐   ┌──────────────────────┐ │
  ┌─────┴──────┐     │  │  Donate to      │   │  View Donation       │ │
  │   Donor    │─────┼─►│  Campaign       │   │  History / Receipt   │ │
  └─────┬──────┘     │  └─────────────────┘   └──────────────────────┘ │
        │            │                                                  │
        │            │  ┌─────────────────┐   ┌──────────────────────┐ │
        │            │  │  Post Comment   │   │  Follow Campaign     │ │
        │            │  └─────────────────┘   └──────────────────────┘ │
        │            │                                                  │
  ┌─────┴─────────┐  │  ┌─────────────────┐   ┌──────────────────────┐ │
  │   Organizer   │──┼─►│  Create /       │   │  Post Campaign       │ │
  └───────────────┘  │  │  Manage         │   │  Update              │ │
                     │  │  Campaign       │   └──────────────────────┘ │
                     │  └─────────────────┘                            │
                     │                                                  │
  ┌───────────────┐  │  ┌─────────────────┐   ┌──────────────────────┐ │
  │ Administrator │──┼─►│  Moderate       │   │  Manage Users        │ │
  └───────────────┘  │  │  Campaigns      │   └──────────────────────┘ │
                     │  └─────────────────┘                            │
                     │                                                  │
  ┌───────────────┐  │  ┌─────────────────┐                            │
  │  AI Chatbot   │──┼─►│  Answer User    │                            │
  │  (RAG)        │  │  │  Queries        │                            │
  └───────────────┘  │  └─────────────────┘                            │
                     └──────────────────────────────────────────────────┘
```

### 9.2 Sequence Diagram — Donation Process

```
Donor         Frontend       Backend API     Stripe API     Database     Email Service
  │               │               │               │              │             │
  │──Click──────►│               │               │              │             │
  │  "Donate"    │               │               │              │             │
  │               │──POST /donations/intent──────►│              │             │
  │               │               │──CreateIntent►│              │             │
  │               │               │◄──Intent ID──│               │             │
  │               │◄──{clientSecret}─────────────│               │             │
  │               │               │               │              │             │
  │◄──Show Stripe │               │               │              │             │
  │  Payment UI──│               │               │              │             │
  │               │               │               │              │             │
  │──Enter card──►│               │               │              │             │
  │  details      │               │               │              │             │
  │               │──confirmPayment──────────────►│              │             │
  │               │               │               │──Process────►│             │
  │               │               │               │◄──Success───│             │
  │               │◄──Payment OK─────────────────│               │             │
  │               │               │               │              │             │
  │               │         (Stripe Webhook fires)│              │             │
  │               │               │◄──POST /webhook──────────────┤             │
  │               │               │  payment_intent.succeeded    │             │
  │               │               │──Verify signature            │             │
  │               │               │──BEGIN TRANSACTION──────────►│             │
  │               │               │──INSERT Donation (completed)─►│             │
  │               │               │──UPDATE campaign raised_amt──►│             │
  │               │               │──COMMIT──────────────────────►│             │
  │               │               │──Send receipt────────────────────────────►│
  │               │               │                              │  Send email │
  │               │◄──Update progress bar         │              │             │
  │◄──Confirmation│               │               │              │             │
  │  page shown──│               │               │              │             │
```

### 9.3 ER Diagram

```
┌──────────────────────┐       ┌───────────────────────┐
│         USER         │       │        CAMPAIGN        │
│──────────────────────│       │───────────────────────│
│ PK user_id (INT)     │──1──┐ │ PK campaign_id (INT)  │
│    username (VAR80)  │     └►│ FK creator_id (INT)   │
│    email (VAR120)    │       │    title (VAR200)      │
│    password_hash     │       │    description (TEXT)  │
│    role (ENUM)       │       │    category (ENUM)     │
│    profile_image     │       │    goal_amount (DEC)   │
│    is_active (BOOL)  │       │    raised_amount (DEC) │
│    is_banned (BOOL)  │       │    start_date (DATE)   │
│    created_at (TS)   │       │    end_date (DATE)     │
└──────────────────────┘       │    image (TEXT)        │
          │   │                │    status (ENUM)       │
          │   │                └───────────────────────┘
          │   │                           │
          │   │ 1:N                       │ 1:N
          │   └──────────────────────┐   │
          │                          ▼   ▼
          │   1:N         ┌──────────────────────┐
          └──────────────►│       DONATION        │
                          │──────────────────────│
          1:N             │ PK donation_id (INT)  │
  ┌──────────────────┐   │ FK donor_id (INT)     │
  │  CAMPAIGN_UPDATE │   │ FK campaign_id (INT)  │
  │──────────────────│   │    amount (DEC)        │
  │ PK update_id     │◄──┤    status (ENUM)       │
  │ FK campaign_id   │   │    is_anonymous (BOOL) │
  │ FK author_id     │   │    payment_ref (VAR)   │
  │    title         │   │    created_at (TS)     │
  │    content       │   └──────────────────────┘
  │    created_at    │               │ 1:1
  └──────────────────┘               ▼
                          ┌──────────────────────┐
  ┌──────────────────┐   │       PAYMENT         │
  │    ADMIN_LOGS    │   │──────────────────────│
  │──────────────────│   │ PK payment_id (INT)   │
  │ PK log_id (INT)  │   │ FK donation_id (INT)  │
  │ FK admin_id      │   │    gateway_response   │
  │    action_type   │   │    created_at (TS)    │
  │    entity_type   │   └──────────────────────┘
  │    entity_id     │
  │    notes         │   ┌──────────────────────┐
  │    performed_at  │   │      COMMENT          │
  └──────────────────┘   │──────────────────────│
                          │ PK comment_id (INT)  │
  ┌──────────────────┐   │ FK user_id (INT)      │
  │   USER_FOLLOWS   │   │ FK campaign_id (INT)  │
  │──────────────────│   │    content (TEXT)      │
  │ FK user_id (INT) │   │    likes (INT)         │
  │ FK campaign_id   │   │    created_at (TS)    │
  │    followed_at   │   └──────────────────────┘
  └──────────────────┘
```

---

## 10. Future Enhancements

The following features are planned for future versions of the platform:

### 10.1 Recurring Donations

Allow donors to set up automatic monthly or weekly contributions to a campaign or an organizer. This requires subscription billing support from the payment gateway (e.g., Stripe Subscriptions) and a scheduler (e.g., Celery + Redis) to trigger periodic charges and update raised amounts.

### 10.2 Social Sharing

Provide one-click sharing of campaign pages to Twitter/X, Facebook, LinkedIn, and WhatsApp, along with Open Graph meta tags for rich link previews. Include a referral tracking system to attribute donations to specific share sources, enabling organizers to measure marketing effectiveness.

### 10.3 Multi-Currency Support

Enable donors to donate in their local currency by integrating Stripe's currency conversion capabilities. Campaign organizers will set a base currency; raised amounts will be normalised to the base currency at the time of donation. The UI will display the donor's local currency equivalent.

### 10.4 Campaign Comments — Enhanced Features

Extend the comment system with: threaded replies, reaction emojis, rich text formatting, and @mention notifications. Implement a community moderation system where donors can upvote helpful comments and flag abusive ones.

### 10.5 Fraud Detection

Implement an automated fraud detection layer that flags suspicious donation patterns (e.g., multiple small donations from the same IP address, unusual velocity) using rule-based heuristics and optionally machine learning models. Integrate with Stripe Radar for payment-level fraud prevention. Suspected fraudulent activities will trigger admin review workflows.

### 10.6 Mobile Applications

Develop native iOS and Android applications using React Native, sharing the core business logic with the web frontend and consuming the same REST API.

### 10.7 Campaign Analytics Dashboard

Provide organizers with an advanced analytics dashboard showing: donation trends over time (line charts), donor geography (map visualisation), traffic sources, social share performance, and conversion funnels from visit to donation.

### 10.8 Notification Centre

Build an in-app notification centre for real-time alerts (e.g., "Your campaign has been funded 50%!", "A new comment on your campaign") using WebSockets or Server-Sent Events.

---

*End of Software Requirements Specification*

*Document Version 1.0 — CrowdFund Platform — IEEE Std 830-1998*
