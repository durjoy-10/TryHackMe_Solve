# TryHackMe — Cache Me Outside

## Room Overview

**Room Name:** Cache Me Outside  
**Category:** OSINT / Active OSINT  
**Platform:** TryHackMe  
**Objective:** Identify a retired hacker by following a trail of public online clues starting from a leaked conversation screenshot.

The room begins with a Discord-style screenshot where two users discuss an old hacking scene, a forum being taken down, and one user moving away from hacking into hiking and cycling. The important clue in the screenshot is a public Komoot profile link.

> **Note:** This room includes controlled active OSINT interaction. In a real-world investigation, contacting targets or interacting with discovered infrastructure/accounts can be risky and should only be done with clear authorization.

---

## Given Starting Evidence

The provided screenshot contains a conversation between two users:

- `WKM1337?`
- `JJ ^_^`

The key message is from `JJ ^_^`, where he says he uses Komoot to track hiking and cycling routes and shares a public profile link:

```text
https://www.komoot.com/user/5667624959835
```

This link becomes the first pivot point for the investigation.

---

## Questions and Answers

| Question | Answer |
|---|---|
| What is the retired hacker’s full name? | `Jim Lee` |
| What email address did he accidentally expose? | `jimleepro1@gmail.com` |
| What is his phone number? | `+40 743 321 239` |
| In which city is he located? | `Timisoara` |
| Submit the name of the tram station where he got off on the 7th of May, 2026. | `Piata Gheorghe Domasneanu` |

---

## Step 1 — Extract the First Clue from the Screenshot

The screenshot shows that `JJ ^_^` is the retired hacker. He mentions that he is now into hiking and cycling and provides a Komoot profile.

The profile URL is:

```text
https://www.komoot.com/user/5667624959835
```

This is important because Komoot profiles often expose:

- Display name
- Username
- Routes
- Activity dates
- Locations
- Linked or reused identity clues

---

## Step 2 — Visit the Komoot Profile

Opening the Komoot profile reveals the identity behind the account.

From the profile, the retired hacker’s name is found as:

```text
Jim Lee
```

This answers the first question.

### Answer

```text
Jim Lee
```

---

## Step 3 — Pivot from Komoot to Other Online Profiles

After identifying the name, the next goal is to find reused usernames or linked profiles.

The Komoot profile gives enough identity context to search for related accounts. The important pivot is the hacker-style username:

```text
jiml33t
```

This username is a likely hacker alias because it uses “leet” spelling:

- `lee` from Jim Lee
- `l33t` as hacker-style spelling of “leet”

Searching this username leads to a GitHub profile/repository connected to the same person.

---

## Step 4 — Investigate the GitHub Repository

The GitHub account/repository contains commits made by the user.

In OSINT, Git commits are very useful because commits often contain metadata such as:

- Author name
- Author email
- Commit timestamp
- Commit message

Even if a profile page does not directly show an email, commit metadata can expose it.

A useful technique is to view a GitHub commit as a patch by appending `.patch` to the commit URL.

Example format:

```text
https://github.com/<username>/<repo>/commit/<commit_hash>.patch
```

The `.patch` view exposes commit metadata in plain text.

Inside the commit metadata, the exposed email address is found:

```text
jimleepro1@gmail.com
```

### Answer

```text
jimleepro1@gmail.com
```

---

## Step 5 — Active OSINT Interaction: Email Contact

The room description states that active OSINT interaction is part of the controlled challenge setup.

After discovering the exposed email address, the next step is to send an email to:

```text
jimleepro1@gmail.com
```

The challenge sends an automated response. This response reveals Jim Lee’s phone number.

The phone number found is:

```text
+40 743 321 239
```

The `+40` country code is also an important clue because it belongs to Romania.

### Answer

```text
+40 743 321 239
```

---

## Step 6 — Determine the City

The Romanian phone number indicates that the target is likely connected to Romania.

Further OSINT pivots from the discovered identity, username, and public social clues lead to Romanian location hints. One clue points toward:

```text
irigato.ro
```

The `.ro` domain reinforces the Romania connection.

Additional location clues from the public profile trail point to the city:

```text
Timisoara
```

TryHackMe’s answer format shows eight characters, and `Timisoara` matches the required format when written without Romanian diacritics.

The Romanian spelling is:

```text
Timișoara
```

But for the room answer format, use:

```text
Timisoara
```

### Answer

```text
Timisoara
```

---

## Step 7 — Find the Tram Station for 7 May 2026

The final question asks for the tram station where Jim Lee got off on:

```text
7 May 2026
```

At this point, the investigation combines:

- The identified city: `Timisoara`
- Public travel/activity clues
- Date-specific activity
- Public transport/tram route context
- Nearby landmarks connected to the trail

The relevant clue points toward an area near a French supermarket/Auchan location in Timișoara.

Checking the nearby tram/public transport stops leads to the tram station:

```text
Piața Gheorghe Domășneanu
```

TryHackMe’s answer format expects plain ASCII without Romanian diacritics:

```text
Piata Gheorghe Domasneanu
```

### Answer

```text
Piata Gheorghe Domasneanu
```

---

## Final Answers

```text
Full name: Jim Lee
Email address: jimleepro1@gmail.com
Phone number: +40 743 321 239
City: Timisoara
Tram station: Piata Gheorghe Domasneanu
```

---

## Investigation Summary

The room starts with a simple leaked chat screenshot, but the screenshot contains a direct Komoot profile link. From that Komoot profile, the retired hacker’s real name is discovered as Jim Lee. Searching related identity clues leads to a GitHub profile using the alias `jiml33t`.

GitHub commit metadata exposes the email address `jimleepro1@gmail.com`. Since the room explicitly allows active OSINT interaction, sending an email to that address triggers an automated response containing the phone number `+40 743 321 239`.

The Romanian country code, combined with public social/location clues, leads to the city `Timisoara`. Finally, date-specific route and location clues for 7 May 2026 point to the tram station `Piata Gheorghe Domasneanu`.

---

## Key OSINT Techniques Used

### 1. Screenshot Analysis

The initial image was inspected for visible usernames, links, and conversational context.

### 2. Profile Pivoting

The Komoot profile link was used to move from a chat alias to a real-world identity.

### 3. Username Reuse

The alias `jiml33t` was used to locate related public accounts.

### 4. GitHub Commit Metadata Analysis

GitHub commits were inspected using `.patch` format to reveal hidden author metadata.

### 5. Controlled Active OSINT

The exposed email was contacted only because the room explicitly states that active interaction is part of the challenge.

### 6. Geolocation

Phone number country code, Romanian domain clues, city references, and transit stop mapping were combined to identify the final location.

---

## Lessons Learned

This room demonstrates how small pieces of public information can connect into a complete identity trail. A single shared profile link can expose names, usernames, activity locations, and linked accounts. GitHub commit metadata is especially important in OSINT because users often accidentally expose personal emails through commit history.

The challenge also shows why operational security matters. Reusing usernames, exposing commit metadata, sharing public activity routes, and responding from personal contact points can all create a traceable online identity.
