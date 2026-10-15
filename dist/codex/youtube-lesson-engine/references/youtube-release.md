# Releasing Lessons and Suno Music on YouTube

Use for a lesson's packaging (title, thumbnail, chapters, description, pinned comment), a selected track's title and description, an artist's channel bio, or questions about releasing music after a Suno subscription ends. This is publishing guidance, not a composition prompt.

## Packaging an AI or tech lesson

Packaging decides whether a lesson gets clicked, and it must also be true. The video has to pay off every title, thumbnail and chapter, and pay off the title's question within the first minute. YouTube's spam and deceptive-practices policies cover misleading titles, thumbnails and descriptions, so a curiosity gap is a question the video answers, never a claim it contradicts. Specific, technical, evergreen topics tend to draw search traffic and advertiser demand; this guide makes no promise about RPM or revenue.

Ground packaging in the manifest and the research notes, and keep perishable claims (versions, prices, rankings) dated.

### Titles: curiosity-gap formulas

Aim for about 60 characters; the manifest validator warns above about 70, where search results often truncate. Put the searchable term (the technology, model, release or repository name) in the first 40 characters. Use one number at most, and capitalise at most one word for emphasis.

| Formula | Pattern |
|---|---|
| The misconception | "[Familiar thing] Doesn't [what people assume]", e.g. "Git Doesn't Store Diffs" |
| The hidden mechanism | "How [product or release] Actually [does the thing]" |
| The concrete cost | "Why [familiar setup] [surprising consequence]" |
| The change | "[Release] Changed [one specific thing]" (date-stamp the release in the notes) |
| The teardown | "Inside [repository]: [the one design choice that matters]" |
| The test | "[Claim], Tested" or "[A] vs [B] on [one specific workload]" |

The title and the thumbnail work as a pair: the thumbnail's words add to the title and never repeat it. The Hook's first sentence should address the title's gap directly.

### Thumbnail: three words, high contrast

- **Format:** 1280×720 (16:9), JPG or PNG, under 2 MB. Custom thumbnails require a verified account. These specs were consistent across sources checked 2026-10-15; Studio shows the current limits.
- **Words:** three at most, adding to the title rather than repeating it ("NOT DIFFS", "SNAPSHOTS ONLY"). One weight, with a cap height of at least 120 px on the 720 px frame (one-sixth of its height).
- **Contrast:** white or the accent colour on a near-black ground, aiming for 7:1 or better, because thumbnails are shown small.
- **Subject:** one focal element taken from the lesson's own visuals: the key diagram node, the decisive code line, the benchmark bar. Use the same design system as the video.
- **Keep clear:** YouTube overlays the video length in the bottom-right corner, so keep that corner empty.
- **Test small:** check the thumbnail at about 168×94 px, roughly a small suggested-video size. If the three words cannot be read there, they are too small or too many.
- **Stay honest:** no fake interfaces, invented numbers, or logos that imply an endorsement.

### Chapters from the timeline

`scripts/generate-tts-and-cues.py` writes `chapters.txt` from the resolved timeline: one chapter for the Hook, one per Mechanism block, one for the Proof and one for the Verdict. Each is titled from its first segment headline, or from the block's slug. A chapter starts after the hook drop, or at the swell that leads into the Verdict.

The generator applies YouTube's chapter rules: the first timestamp is 0:00, there are at least three, they ascend, and each chapter lasts at least 10 seconds. Shorter chapters merge into their neighbour, and with fewer than three it writes none. These rules were checked 2026-10-15 against summaries of YouTube's "Video chapters" help article; recheck there. Chapters can still fail to appear on a channel with active strikes.

Paste the list into the description. Titles may be edited for curiosity but must stay true to their section. If the edit changes after rendering, regenerate the timeline instead of shifting timestamps by hand.

### Description template

The first lines appear before "more", so lead with the payoff.

```
[One sentence answering the title's question, including the searchable term.]
[One sentence on what the viewer sees: the mechanism and the proof.]

Chapters
[paste chapters.txt]

Sources (checked [date])
- [primary source]
- [primary source]

[Repository, code or cheat-sheet link]

Narration: AI voice (ElevenLabs). Music: made with Suno.
#[topic] #[technology]
```

A credit line in the description does not replace the Studio disclosure setting (see "YouTube AI disclosure" below).

### Pinned-comment templates

Pin one comment per lesson. Promise only what the link delivers and check that every link works. If the link collects email addresses, follow the consent and privacy rules that apply to you; at minimum that means a privacy notice and an unsubscribe option.

1. **Resource:** "The [diagram / cheat sheet / code] from [m:ss] is here: [link]. [One line on what is inside.] Free, no sign-up."
2. **Question:** "Question for you: [a specific question the Verdict raises]? The best answer gets pinned on the next lesson."
3. **Newsletter:** "One teardown like this every [week], in your inbox: [link]. [What subscribers get that the video does not.] Unsubscribe anytime."
4. **Next lesson:** "Next: [follow-up lesson title], which answers [the open question this lesson leaves]. [Link, or subscribe to catch it.]"

## Music releases

### Ground the copy in the work

Use the artist name, selected song, public profile and user-provided production details. Read a linked song page when available. Separate genre tags and lyrics from listening evidence: reading metadata is not hearing the track, and a screenshot of an upload is not watching the video.

Deliver copy ready to paste:

- **Title:** Artist - Track | Music Video. Use "Official Music Video" only for the artist's own authorized release.
- **Video description:** A short hook grounded in the song's theme, title and artist, a concise genre or mood description, accurate production credits, a listening/profile link and an optional invitation to subscribe. A few relevant hashtags are optional.
- **Channel bio:** Who makes the music, the musical territory, what viewers can expect and where to hear more. Mention AI plainly without apologizing for it or inventing human performance credits.

Do not invent lyric authorship, vocal performance, instruments played, visual tools, a release schedule or a public launch. Keep subscription history and licensing explanations outside the promotional copy unless the user wants them included. Do not automatically add copyright, exclusivity or "all rights reserved" claims.

Keep artist-specific copy in the user's durable release folder, not this reusable reference. Record whether it is drafted, entered in Studio, saved, public or otherwise verified. A request to write copy does not itself authorize publishing or modifying an external account.

## Suno rights: use the plan at creation time

Policy checked **2026-10-14**. Recheck the official sources below for later release decisions; this note is not a permanent guarantee.

Suno's help guidance says a song created while subscribed to **Pro or Premier** retains commercial-use rights after the subscription ends. A creator does not need to restart a subscription solely to release that qualifying track. Their current free-plan status does not erase those rights.

Conversely, a later paid subscription does not automatically grant commercial rights to songs originally created on the free plan. Free-plan songs are restricted to non-commercial use under Suno's guidance. Extensions or reused third-party material can require separate assessment; do not assume a paid edit clears the source material.

Use the user's account of their subscription timing as an attributed fact, not independently verified billing evidence. Where available, retain the song identifier, creation date and relevant subscription record privately with the release. Do not put billing evidence in descriptions or reusable skill files.

Commercial-use permission from Suno is distinct from statutory copyright protection, permission for third-party material and YouTube monetization eligibility. Avoid turning a narrow subscription question into an unsupported guarantee about all three.

Official sources:
- [Does Suno own the music I make?](https://help.suno.com/en/articles/2416769)
- [If I subscribe, do I get rights for songs made before subscribing?](https://help.suno.com/en/articles/2425729)
- [Who owns an extension?](https://help.suno.com/en/articles/2871105)

## YouTube AI disclosure

Policy checked **2026-10-14**. YouTube's guidance requires disclosure when AI creates music that is the main focus of a video. For a Suno music video, select **Yes** in Studio's **AI use** setting; some interfaces may still call it **Altered content**. Verify the current interface label when operating Studio.

**Lesson videos.** Rechecked 2026-10-15 through search results that summarise the official page; confirm on the page itself. YouTube lists synthetically generating a person's voice to narrate a video among the examples that require disclosure, and productivity uses such as AI-drafted scripts or automatic captions among those that do not. A lesson narrated by an ElevenLabs voice should therefore select **Yes**. A lesson narrated in the creator's own recorded voice, with Suno music only as a background bed, is not clearly covered by the music example above, which concerns AI music that is the main focus of the video. When unsure, disclose.

Mentioning Suno or AI in a description does not replace the upload disclosure setting. YouTube says disclosure itself does not restrict the audience or affect eligibility to earn money; this does not promise monetization approval for a particular video or channel.

Official source:
- [YouTube: Disclosing use of GenAI content](https://support.google.com/youtube/answer/14328491?hl=en)

## Release record

Keep the selected audio/video identity, final copy, source links, date of policy verification, any rights evidence and actual upload/publication state beside the release materials. Preserve local evidence there rather than citing temporary screenshot paths. Record drafts as drafts until saving or publication has been confirmed.
