# PDD: Submit expense claims into ExpenseFlow

**Raised by:** Finance Operations, month-end close
**For:** RPA team
**Priority:** Normal. Month-end is in two weeks.
**Reference:** FIN-2291
**Document:** Process Design Document (PDD)

---

## What we do today

At month-end I get a spreadsheet of expense claims from the cost-centre leads
and type them into ExpenseFlow one at a time. Last month there were 340. It takes
the best part of two days and I make mistakes when I'm tired.

The spreadsheet is always the same shape. This month's is in
`Data/expenses.xlsx`. For this work please use the practice copy of the portal at
`assets/expenses.html`. It behaves the same as the real one and doesn't touch
live data.

## What I'd like

Take the spreadsheet, put every claim into the portal, and tell me what happened
to each one.

## Detail

**Open the portal yourself.** Don't expect it to be open when the run starts. Open
it at the start, in the default browser on the machine, and leave it open when
you finish. I want to look at the submissions table afterwards, and if it closes
the table goes with it.

**Each row is one claim.** Employee ID, date, category, amount, currency,
whether a receipt is attached, and any notes. They go into the matching fields
on the portal form.

**Check each claim before you submit it.** The policy rules are already written
down in the process. Use that check rather than a new copy of the rules, and
don't submit anything it rejects. Compliance reads the portal's rejection log and
asks why we filed a claim we knew was non-compliant, and every refused submission
is a wasted round trip. Record those as rejected, with the reason, and carry on.

**One browser session for the whole file.** Don't reopen the portal for each
row. It's slow, and the confirmation numbers restart if the page reloads.

**The portal checks too.** It enforces the same policy, so if our check misses
something it will refuse the claim:

- An expense of 50.00 or more with no receipt attached (policy PL-114).
- Anything in the Other category with no note (policy PL-118).

It shows a rejection message on screen and does not file the claim.

**A refusal is not a failure.** This is the part I care about most. Last time
somebody automated one of these it stopped dead on the first rejected row and I
found out three hours later. If a claim is refused, note the reason, move to the
next row, and keep going to the end.

**I need the confirmation numbers.** An accepted claim gets a number like
`EXP-0001`. Audit asks for these, so record each one against the right claim.
The number doesn't appear instantly. The portal takes a moment to file the claim,
so make sure you read the real one and not whatever was on screen a second
earlier. That has bitten us before.

**Give me a summary I can open.** One row per claim: who it was for, the amount,
whether it went through, its confirmation number if it did, the reason if it
didn't. We already write a spreadsheet to `Data/summary.xlsx`. Extend that.

## How I'll check it

Run it against this month's six-row file:

1. The portal's submissions table shows the claims that should have gone
   through, and only those.
2. The summary has all six rows, and every rejection has a reason I can read out
   to the cost-centre lead who filed it.

## Not needed

- Don't email anyone.
- Don't try to fix rejected claims. That's a conversation with a person.
- Don't worry about the 340-row file. Get six right first.

## Notes from the RPA team

The portal is a single self-contained page with stable element ids, listed in a
comment at the top of `assets/expenses.html`. Use them. The previous attempt
targeted fields by position and broke the first time someone added a field.

It's a local file, so the browser needs an absolute `file://` URL, not the
relative path above.

The run uses whichever browser the targets were captured in. That browser needs
the UiPath extension, with access to file URLs turned on.

The date field is a native date picker. What you type into it depends on the
browser's locale, not on how the spreadsheet stores the date. Check it on the
first row.
