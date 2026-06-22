# Cold email playbook

A cold email earns a reply when a stranger recognizes their own problem in the
first two lines and sees one easy next step. Most cold email fails not on the
offer but on the craft: the wrong person, the wrong opener, three asks, no
follow-up. This playbook is the depth behind the six steps in SKILL.md.

The skill **drafts** emails and sequences. Sending is an external mutation
against real recipients and a sender reputation, so a human approves and sends
every message. Nothing here authorizes an automatic send.

## The anatomy of a cold email

A cold email has six parts, in order. Each part has one job, and a part that
does two jobs weakens both.

1. **Subject line** — earns the open. Three to five words, lowercase or
   sentence case, no clickbait, no false "Re:" or "Fwd:". The subject names the
   recipient's world, not the sender's product. Good: "question about your
   onboarding". Bad: "ACME Pro — 40% off this week!!!".
2. **Opener / personalization** — earns the next sentence. One line that proves
   the email was written for this person: a recent hire, a launch, a podcast
   quote, a number from their site. The opener is a fact about *them*, never a
   compliment ("love what you're building") and never a template variable left
   raw.
3. **Problem** — names a pain the recipient already feels. One or two sentences,
   in the recipient's language, tied to the trigger from the opener. A problem
   the reader does not recognize reads as a pitch.
4. **Value** — one sentence on the outcome, not the feature. State the result a
   similar customer got, with a number when an honest one exists. "Cut payroll
   reconciliation from 3 days to 3 hours for a 200-person team" beats "powerful
   automation platform".
5. **Single CTA** — one ask, low-friction, easy to say yes to. A yes/no
   interest check ("worth a look?") or a soft time ask ("open to 15 minutes next
   week?"). One CTA per email is a hard rule (see below).
6. **Sign-off** — a real name, a real company, a physical address, and a working
   one-click opt-out. The sign-off carries the compliance payload and the proof
   that a person, not a bot, stands behind the message.

Length target: 50–125 words. A cold email read on a phone in five seconds has no
room for a second paragraph of setup.

## Personalization tiers

Personalization is a cost. The right tier depends on the deal size and the list
size, not on a blanket "always personalize" rule.

| Tier | What it means | Cost per email | Pays off when |
|------|---------------|----------------|---------------|
| **None (mass)** | Same body to a broad list; only the name merges in | Seconds | Low ACV, huge addressable list, offer is self-evidently relevant to the whole segment |
| **Segment** | One template per tightly-defined segment; opener references a trait the whole segment shares (industry, stack, role, recent event) | Minutes per segment | Mid ACV; the segment is narrow enough that one trigger is true for every recipient |
| **1:1** | Opener researched per person; a sentence that could only have been written for them | 10–20 minutes per email | High ACV, named-account or executive outreach, small list where one reply funds the effort |

The dominant failure is mismatch: 1:1 effort sprayed across a 10,000-row list
(unscalable), or a mass blast sent to ten dream accounts that each deserved a
researched note (wasteful). Match the tier to the economics before drafting.

A segment-tier opener still must read as specific. "As a fintech company" is not
personalization; "now that the EU instant-payments mandate hits in 2025" is.

## Deliverability and spam triggers

A perfect email in the spam folder converts at zero. Deliverability is a
precondition, not a polish step.

**Sender setup (done once, before any volume):**

- Authenticate the domain with SPF, DKIM, and DMARC. A missing record sends mail
  straight to spam at most providers.
- Send from a dedicated outreach subdomain (e.g. `mail.acme.com`), never the
  primary domain that carries transactional and personal mail. A burned
  subdomain protects the root domain.
- Warm the domain: ramp volume over 3–4 weeks, starting near 10–20 sends a day
  and climbing gradually as positive engagement accrues. A cold domain that
  sends 1,000 on day one gets flagged.

**Per-message triggers to avoid:**

- **Links** — zero or one link maximum. Two or more links in a cold email is a
  strong spam signal. A bare tracking pixel plus a link compounds the risk.
- **Attachments** — none. A cold email with an attachment is filtered hard and
  often is unsafe to open from a stranger.
- **Spammy words** — avoid "free", "guarantee", "act now", "limited time",
  "100%", "$$$", "click here", and ALL CAPS. Exclamation points stack as a
  signal; cap at zero or one.
- **Image-heavy or all-HTML bodies** — plain text (or near-plain) outperforms a
  templated HTML banner and dodges the "marketing blast" classifiers.
- **Volume and velocity** — keep per-inbox daily volume modest (a common ceiling
  is 30–50 cold sends per inbox per day) and randomize the send timing. A
  thousand identical sends in one minute is a bot fingerprint.
- **Spintax that breaks** — broken merge tags ("Hi {first_name},") are the
  loudest "this is automated" tell and tank reply rates.

**Health to watch:** bounce rate under 2–3% (verify the list first), spam-
complaint rate under 0.1%, and a positive reply rate. A rising bounce or
complaint rate means the list quality or the warmup failed; pause and fix before
scaling.

## The one-CTA rule

One email, one ask. Every additional CTA splits the reader's attention and
lowers the odds of any action — a documented decision-paralysis effect. "Reply,
or book a call, or check out our pricing page, or follow us" is four asks and
zero clarity.

Pick the single lowest-friction next step the deal stage justifies:

- Cold first touch → an interest check ("worth a quick look?"). Asking for 30
  minutes from a stranger is too big a first ask.
- Warm or replied → the meeting ask, with a concrete window.

The CTA is a question the reader can answer in one word or one click. A CTA that
requires the reader to think about *how* to respond is friction.

## The follow-up sequence

The single most common cause of a dead campaign is no follow-up. A large share
of replies arrive on the second through fourth touches, not the first. A
sequence is not nagging when each touch adds a new angle.

**Cadence** (business days, not calendar days):

| Touch | Day | Angle |
|-------|-----|-------|
| 1 | 0 | Initial email: trigger + problem + value + soft CTA |
| 2 | +3 | Short bump: new angle or a one-line proof point, not "just bumping this" |
| 3 | +7 | Different value angle — a case study, a resource, a different pain |
| 4 | +14 | The break-up: "closing the loop, should I assume the timing is off?" |

Rules for the sequence:

- Each touch is shorter than the last. Touch four is two sentences.
- Each touch carries one new piece of information; a pure "following up" adds
  nothing and reads as pressure.
- Reply to the same thread so context travels with the message.
- One CTA per touch, same as the first email.
- Stop on any reply, on an opt-out, or after the break-up. Four to five touches
  is the normal ceiling; more reads as harassment and risks complaints.

## Compliance

Cold outreach is legal in most jurisdictions when done right, and a fast path to
a blocklist when done wrong. Treat the rules below as the floor, not legal
advice; a regulated industry or a specific country may demand more.

**CAN-SPAM (United States), the practical checklist:**

- Accurate "From", "To", and routing — no spoofed or misleading sender.
- A subject line that does not deceive about the content.
- A clear, working opt-out mechanism in every message.
- Opt-out requests honored within 10 business days, and the address suppressed
  permanently after.
- A valid physical postal address in the footer.
- Disclosure that the message is an outreach/commercial message where required.

**GDPR / PECR (European Union and United Kingdom), the practical checklist:**

- A lawful basis for processing the contact's data — for B2B cold email this is
  usually *legitimate interest*, which demands a relevance balancing test and a
  record of it.
- Personal data (the email address, any enrichment) handled per the regulation:
  collected for a stated purpose, retained no longer than needed.
- A clear opt-out and an easy route to exercise data-subject rights
  (access, erasure).
- Sender identity and purpose stated plainly in the message.
- Some member states require prior consent even for B2B; check the destination
  country before sending there.

**Universal:** keep a suppression list, honor every unsubscribe immediately,
never email a purchased or scraped list of consumers, and verify addresses to
keep bounces low. Compliance and deliverability reinforce each other — the
sender who respects opt-outs keeps a clean reputation.

## Failure modes

These four patterns kill more campaigns than a weak product does.

- **The pitch-slap** — leading with the product before naming a problem the
  reader feels. The reader's first thought is "who are you and why do I care",
  and the email dies in line one. Fix: open on their trigger and their pain,
  reach the product only after.
- **All-about-us** — every sentence starts with "we" / "our" / the company name.
  The reader is the protagonist of their inbox; a self-centered email gets
  archived. Fix: count the "you/your" versus "we/our" ratio and keep it tilted
  toward the reader.
- **Multi-CTA** — two or more asks in one email. The reader picks none. Fix: cut
  to the single lowest-friction next step.
- **No follow-up** — one touch and silence. The campaign forfeits most of its
  potential replies. Fix: build the sequence before sending touch one, so the
  follow-ups are queued and not improvised.

## Red flags

A draft trips a red flag when any of these is true:

- The opener would be true for any company in the list (not actually
  personalized).
- The body exceeds ~125 words or runs past one screen on a phone.
- Two or more links, any attachment, or a spam-trigger word survived the check.
- More than one CTA, or a first-touch CTA that asks for a large time commitment.
- The footer is missing a physical address or a working opt-out.
- The sequence has one touch, or a follow-up that says only "bumping this".
- The "you/your" count is lower than the "we/our" count.
- The sender domain is the primary domain, unauthenticated, or unwarmed.

Each red flag maps to a specific fix above. A draft with an unresolved red flag
is not ready for the user to send.

## Worked example: a 3-email sequence

**Context.** Founder sells a payroll-reconciliation tool. ICP: heads of finance
at 100–300-person SaaS companies. Trigger: the company recently posted a senior
accounting role (a signal that finance ops is straining). Tier: segment, with a
1:1 opener line.

**Email 1 — Day 0**

> Subject: that senior accountant role
>
> Hi Dana — saw Northwind just opened a senior accountant req. Usually that
> means month-end close is eating the team's evenings.
>
> Finance teams your size tell us reconciliation is the worst of it — matching
> payroll across systems by hand. We got Brightloop's close from 3 days to 3
> hours without adding headcount.
>
> Worth a quick look?
>
> — Lucas, Acme Payroll · 123 Market St, San Francisco, CA · unsubscribe

Why it works: subject names her world; opener is a real trigger; problem is in
her language; value is one outcome with a number; one soft CTA; compliant
footer. ~70 words, zero links, plain text.

**Email 2 — Day +3 (same thread)**

> Subject: Re: that senior accountant role
>
> One more data point, Dana: Brightloop ran the same close with one fewer
> contractor after switching.
>
> Still worth 15 minutes?
>
> — Lucas

Why it works: shorter; a new proof point, not "just bumping"; one CTA; same
thread.

**Email 3 — Day +14 (the break-up, same thread)**

> Subject: Re: that senior accountant role
>
> I'll close the loop here, Dana — sounds like the timing isn't right. If
> month-end gets painful again, my door's open.
>
> — Lucas · unsubscribe
>
> (P.S. happy to send the Brightloop case study if it's useful later.)

Why it works: graceful exit; reopens a door without pressure; honors that the
sequence ends here; keeps the opt-out. The break-up email often pulls the
highest reply rate of the three.
