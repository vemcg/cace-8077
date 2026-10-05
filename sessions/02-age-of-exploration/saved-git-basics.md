# Maya and the Magic Save Button

*A story about how to keep your software safe, undo mistakes, and share it with the world, without ever typing a scary command.*

---

## Chapter 1: The Day Everything Broke

Maya had been working on her website for three weeks. It was called **Garden Buddy**, and it helped people figure out when to plant tomatoes, beans, and sunflowers. She had never written a line of code. Instead, she talked to her AI coding partner, and the AI built everything.

On a Tuesday evening she typed:

> **Maya:** The page looks great! Can you change the green color to a darker green, and also move the planting calendar to the top?

The AI did it. But when Maya refreshed the page, the planting calendar was gone. The whole middle of the page was blank.

> **Maya:** Oh no. Undo that! Go back to how it was five minutes ago!
>
> **AI:** I'd love to, but I have a problem. I changed several files, and I didn't keep a copy of the old versions. I can try to rebuild what it looked like from memory, but I might get it wrong. Maya, this is a good moment to talk about something that will protect you for the rest of your software-making life. It's called **version control**.
>
> **Maya:** Version... control? That sounds like something with a lot of buttons.
>
> **AI:** It sounds scarier than it is. Let me explain it with a story about video games.

### The video game save

> **AI:** Have you ever played a video game where you could save your progress? Imagine you're about to fight a big dragon. Before you do, you save the game. If the dragon wins, you don't have to start the whole game over. You just go back to your save and try again.
>
> Version control is a **save button for your whole project**. Every time you reach a good spot, like "the page looks nice" or "the calendar works," we press save. The save keeps a snapshot of every file exactly as it was at that moment. And we never throw away old saves. You can have hundreds of them, lined up like pages in a photo album, each one labeled with a date and a short description.
>
> If something goes wrong, we don't panic. We open the album, find the last good photo, and put things back the way they were.
>
> **Maya:** So I could have gotten my calendar back?
>
> **AI:** Yes, in about ten seconds, if we had been saving. Let's start now so this never happens again.

Here is what Maya learned in that conversation, in both directions.

> **If I want to...** protect my work so I can undo mistakes, change my mind, and look at old versions,\
> **...I should ask the AI to:** "Set up version control for my project."
>
> **If I ask the AI to** set up version control,\
> **...then this will happen to my software:** nothing visible changes. Your website or app looks and works exactly the same. The AI just starts keeping a hidden photo album of your project's history in a secret folder inside it.

The AI also explained the tool's name:

> **AI:** The tool we'll use is called **Git** (say it like "get" with an i, so "git"). It's free, and almost every software team in the world uses it. I'll run it for you. You never have to touch it.

## Chapter 2: Setting Up the Photo Album

> **Maya:** Okay. What do I do?
>
> **AI:** Just say yes. I'll handle everything.

Maya typed: **"Yes, please set up version control for Garden Buddy."**

The AI replied:

> **AI:** Done! Here's what I just did, in plain English.
>
> First, I checked whether Git was installed on your computer. It was, so there was nothing to download. If it hadn't been, I'd have installed it myself or told you exactly which button to click.
>
> Second, I turned your Garden Buddy folder into what's called a **repository**. That's a fancy word, so let me explain it properly. A repository, or "repo" for short, is just a project folder that has a photo album attached to it. The folder holds your files, and the album holds every saved version of them. People usually say "repo" instead of "repository." If someone says "send me the repo," they mean "send me the project folder with all its history."
>
> Third, I told Git who is making the saves. Every save in the album is signed with a name and an email address, like writing your name on the back of a photo. I used the name "Maya" and the email you gave me for your class account.
>
> **Maya:** Where is the album? I don't see anything new in my folder.
>
> **AI:** It's hidden on purpose, so nobody messes it up by accident. It's a folder called `.git`, with a dot at the front. Dot-folders are usually invisible. Please don't open it, move it, or delete it. If you delete it, the whole history disappears and your project goes back to having no memory. That would be like tearing the photo album out of the house and throwing it away.

> **If I want to...** start keeping a history of my project,\
> **...I should ask the AI to:** "Set up version control (git) in this project."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** a hidden folder called `.git` appears inside your project. Your actual files are untouched. From then on, the AI can save snapshots and restore them.
>
> **A warning that goes both ways:** if you ever delete or move the hidden `.git` folder, you lose all your saves. If you ask the AI to "start fresh" with version control, make sure you really want to throw away the old history.

## Chapter 3: Taking Your First Photo (Adding and Committing)

> **AI:** Now let's take our first picture. In Git, taking a picture has two steps, and I'll explain each one with a story.
>
> Imagine you're moving to a new house and packing boxes. First, you walk around and decide **what goes in the box**. Maybe the plates go in, but the trash doesn't. Second, you **tape the box shut and write a label on it**, like "Kitchen stuff, packed Tuesday."
>
> Git works the same way.

### Step 1: Adding (choosing what goes in the box)

> **AI:** When I "**add**" a file, I'm telling Git, "This file should go in the next picture." The place where files wait for the picture is called the **staging area**. Think of it as a table next to the box, where you set out the things you're about to pack.
>
> Why have this step at all? Because sometimes you've changed ten files, but only three of them belong together. Maybe you fixed the calendar in three files and also half-finished an experiment in the other seven. Adding lets me pick only the calendar files for this picture, so each picture tells one clear story.
>
> For our first picture, though, I'll add everything. It's the very beginning.

### Step 2: Committing (sealing the box and labeling it)

> **AI:** Now I "**commit**" the picture. A **commit** is one saved snapshot in your photo album. It's the sealed, labeled box. Every commit has three things: a snapshot of all the files as they are right now, a label that I write describing what changed, and a date, time, and name.
>
> The label is called a **commit message**. A good one is short and says what changed and why. For example, I'll write: *"First version of Garden Buddy: home page with planting calendar."* Months from now, when you're hunting for the version where the calendar worked, you'll thank yourself for good labels.

Maya watched as the AI did it, and then the AI showed her the album:

> **AI:** Here's your history so far. It has one entry:
>
> *Today, 6:42 PM. Maya: First version of Garden Buddy: home page with planting calendar.*
>
> That's one safe snapshot. The calendar is in it. Even if I break everything tomorrow, that picture is safe forever.
>
> **Maya:** But wait, the calendar is already broken right now, remember? Did you just save the broken version?
>
> **AI:** Good catch, and this is why we commit *good* moments. I saved what's on your screen right now, which includes the blank calendar. Let me fix the calendar first, and then I'll commit again. After that, your album will show a picture of the broken version and then a picture of the fixed version. Both are kept. Nothing is ever erased from the album.

The AI fixed the calendar, Maya checked the page, and it worked. Then:

> **AI:** The calendar is back! I'll commit it now with the message "Fix blank calendar." Now the album has two pictures.

> **If I want to...** save my progress at a good moment,\
> **...I should ask the AI to:** "Save my work" or "Commit what we have with a clear message."
>
> **If I ask the AI to** commit,\
> **...then this will happen:** a new snapshot is added to the end of the album. Your files don't change at all. You just gain a new safe spot you can return to later.

> **If I want to...** see what's been happening in my project,\
> **...I should ask the AI to:** "Show me the history of my project in plain English."
>
> **If I ask the AI to** show the history,\
> **...then this will happen:** you get a readable list of every save, newest first, with its label, date, and who made it. Nothing is changed. It's like flipping through the photo album.

> **If I want to...** know whether I've changed things since the last save,\
> **...I should ask the AI to:** "Tell me what's changed since my last save."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** the AI lists which files are new, which were edited, and which were deleted, without changing anything.

## Chapter 4: Things That Should Never Go in the Album

A few days later, Maya added a feature: Garden Buddy could look up the weather for her city. To do that, it needed to talk to a weather service on the internet. The weather company had given Maya a special secret code, called an **API key**. The AI explained what that meant.

> **AI:** An **API key** is like a password that proves to the weather company that it's really your app asking for the weather. It's long and looks like random gibberish. If a stranger gets it, they can use your account, and sometimes you get charged money for what they do. So an API key is a secret.
>
> Right now, the key is in a small file in your project called `.env`. That's the file I created to hold your secrets.
>
> **Maya:** Okay, so we save everything, right? Including that file?
>
> **AI:** No! This is important. Remember how every picture goes into the album forever? If we put a secret in the album, it's in there forever, even if we delete the file later. And in a little while, we're going to share our album with the world on GitHub. Anything in the album can be seen by everyone who sees the album.
>
> So we need a way to tell Git, "Never take pictures of these things." That's the job of a special file called **.gitignore**.

### What is a .gitignore file?

> **AI:** Picture a photographer at a birthday party. You hand her a list: *"Don't photograph the messy kitchen, don't photograph the bathroom, and don't photograph the private diary on the table."* The `.gitignore` file is that list. It's a plain text file where each line names something Git should pretend doesn't exist.
>
> There are three kinds of things we usually put on the list:
>
> **1. Secrets.** Passwords, API keys, and anything private. Like your `.env` file.
>
> **2. Things that can be rebuilt.** When I build your app, the computer creates lots of extra files automatically. There might be thousands of them, and they're bulky. Since the computer can recreate them anytime, there's no point saving them. Usually these live in folders with names like `node_modules` or `build`.
>
> **3. Computer clutter.** Things your computer makes by itself that have nothing to do with your project, like `.DS_Store` on a Mac or `Thumbs.db` on Windows.
>
> I'll set up the list for you, and I'll add to it whenever a new secret or pile of clutter shows up.

The AI set up the `.gitignore` file and then proved it worked:

> **AI:** I added `.env` to the ignore list. To double-check, I asked Git whether it can see the `.env` file. It said no, so it's invisible to Git. Your secret is safe from the album.
>
> **Maya:** What if I already saved a secret in the album by mistake?
>
> **AI:** Good question, and an honest answer: it's trickier. Just deleting the file isn't enough, because the old picture still has it. The safest fix is to treat that secret as stolen. I would go to the weather company's website with you, cancel that key, and make a new one. Then I would hide the new one properly. If it ever happens, tell me right away. Don't wait, and don't be embarrassed. It happens to professionals too.

> **If I want to...** keep a password, key, or private file out of my history,\
> **...I should ask the AI to:** "Make sure all my secrets are in the ignore list, and double-check that Git can't see them."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** Git will skip those files when saving and when sharing. They stay on your computer, working normally, but they never enter the album.
>
> **A warning in the other direction:** because ignored files are *not* in the album, they are also *not* protected by it. If your computer dies, your secrets are gone with it. Ask the AI to remind you where to find a fresh key, or store the key in a password manager.

> **If I want to...** stop my album from filling up with junk files,\
> **...I should ask the AI to:** "Add the build clutter and computer junk to the ignore list."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** your saves get smaller and faster, and the history shows only things that matter.

## Chapter 5: Why Save Often?

By Friday, Maya had added a "My Garden Journal" page, a photo uploader, and a button for sharing. And the AI was committing after every small step.

> **Maya:** You save so many times! Isn't that overkill? Wouldn't it be neater to do one big save at the end of the week?
>
> **AI:** It would be neater, but it would be much less safe. Let me explain with two stories.
>
> **Story one: The hiker.** Imagine hiking up a mountain and leaving a trail of bread crumbs behind you. If you get lost, you can follow the crumbs back to the last place you knew where you were. If you leave a crumb every ten steps, you're never far from a safe spot. If you only leave one crumb at the very end, you're lost the moment something goes wrong.
>
> Small, frequent saves mean that when something breaks, you only lose a few minutes of work instead of a whole week.
>
> **Story two: The detective.** Suppose the Journal page breaks. If I made a hundred changes in one big save, finding which change caused the problem is like searching a haystack. But if I saved after every small change, I can say, "It worked at save number 41 and broke at save number 42." That tells us exactly where to look.
>
> **Maya:** So the more saves, the better?
>
> **AI:** The rule of thumb is to save whenever something works and you'd be sad to lose it. A finished button, a fixed problem, a new page that loads. I'll do this automatically. You don't need to remind me, but you can always say, "Save this, it's perfect," and I'll make a labeled commit right then.

> **If I want to...** be able to find exactly when something broke,\
> **...I should ask the AI to:** "Save after every small working step."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** your album has many small pictures. It's easy to pinpoint, undo, or study any one change. The cost is a longer list, which is totally fine.
>
> **A warning:** don't ask the AI to save when things are broken and you haven't said so. If you do, the picture captures the broken state. It's not a disaster, since you can always go back further, but the label should say so, like "Calendar is broken, in the middle of fixing."

## Chapter 6: Going Back in Time (Undoing Mistakes)

On Saturday morning, Maya had a bright idea.

> **Maya:** I want the whole page to look like a medieval map! Fancy fonts, parchment colors, everything.
>
> **AI:** Fun! Let's do it.

An hour later, the page was covered in swirly writing and brown textures. Maya squinted at it.

> **Maya:** ...It's hard to read. And kind of ugly. I changed my mind. Can we go back?
>
> **AI:** Absolutely. And because we've been saving, you have options. There are three different "undo" situations, and I'll walk you through each one.

### Situation 1: "I haven't saved the changes yet, and I want to throw them away."

> **AI:** This is the easiest. We made lots of changes this morning, but we haven't taken a picture of them yet. So the last album picture, the one before the medieval makeover, is still perfectly good. I can simply tell Git, "Put every file back the way it looked in the last picture." All the medieval changes vanish. It's like erasing everything you did since the last save.
>
> **But be careful:** this throws away the changes for good, because they were never saved in the album. That's why I always ask you before I do it.

> **If I want to...** throw away what I've done since my last save,\
> **...I should ask the AI to:** "Discard all my unsaved changes and go back to my last save."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** your files snap back to the last saved picture. Everything done since then is **gone and cannot be recovered**, because it was never in the album.

### Situation 2: "I already saved the changes, but I want to undo them."

> **AI:** Let's say we had saved the medieval makeover and then changed your mind. Git has a clever method called a **revert**. When I revert a save, I don't erase it from the album. Instead, I add a *new* picture that is the exact opposite of the old one. If the old save said "made everything parchment brown," the new save says "un-made everything parchment brown."
>
> The nice thing about a revert is that history is never rewritten. The album shows what happened: we tried something, then undid it. Nothing is hidden or lost, so you can even change your mind *again* and bring the medieval look back later.

> **If I want to...** undo a specific change I already saved, without losing the record of it,\
> **...I should ask the AI to:** "Undo the save called 'Medieval map makeover,' but keep it in the history."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** a new save appears that reverses the old one. Your site goes back to how it looked before that change. The old save stays in the album, so you can see it or reuse it later.

### Situation 3: "I just want to *look* at an old version."

> **AI:** Sometimes you don't want to undo anything. You just want to peek. Maybe you remember a design you liked from last Tuesday, and you want to see it. I can set your project to look like last Tuesday for a little while. Then, when you're done looking, I put everything back to today's version. It's like borrowing a time machine for a visit and then coming home.

> **If I want to...** look at what my project looked like on a certain day,\
> **...I should ask the AI to:** "Show me what the project looked like last Tuesday. Don't change anything permanent. I just want to look."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** your files temporarily look like they did then. As long as we make no new changes, I can switch you back to the present with nothing lost. (Tell me if you *do* want to keep something from the old version, and I'll copy it forward.)

### Bonus: "I want just one old file back."

> **AI:** If only one file went bad, I don't need to travel the whole project back in time. I can fetch just that file's old version, like pulling one photo out of an old album, and put it into today's project. The other files stay as they are.

> **If I want to...** get back just one file the way it used to be,\
> **...I should ask the AI to:** "Bring back the old version of the Journal page from before this morning. Leave everything else alone."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** only that one file changes. The rest of your project is untouched.

## Chapter 7: Branches (Trying Big Ideas Safely)

> **Maya:** The medieval look was a flop. But I still want to try a *big* redesign, with a dark mode and a new menu. I'm scared I'll wreck what works.
>
> **AI:** That's exactly what **branches** are for. And I have a good story for you.
>
> Imagine you're writing a school essay on paper. You like your essay as it is, and you don't want to scribble all over it. So you photocopy it. You do your experimenting on the copy. If your experiment makes the essay better, you copy the improvements back onto the original. If it makes the essay worse, you throw the copy in the trash, and the original is exactly as you left it.
>
> A **branch** is a parallel copy of your project where you can experiment safely. In Git, the main version of your project, the one you trust and show to people, is usually called the **main branch** (or just "main"). Think of it as the trunk of a tree. A new branch is a limb growing off the trunk, where you can try new things without disturbing the trunk.

### How branches work

> **AI:** Here's how it goes:
>
> 1. **Make a branch.** I'll say, "Let's make a branch called `dark-mode`." Now we have two lines of history that begin at the same place.
> 2. **Switch to the branch.** I move your working folder over to the `dark-mode` branch. Now when I change files, I'm only changing things on that limb. Main stays the way it was.
> 3. **Work and save on the branch.** I make dark mode and commit as I go. Each commit goes only on the branch. If you look at your main branch during this time, you'll see nothing has changed.
> 4. **Decide.** If we love the result, we **merge**. If we hate it, we **delete the branch**.

### Merging: bringing the good ideas home

> **AI:** To **merge** means to take everything new from the branch and combine it into main. It's like stapling the improved pages from your photocopy into your original essay. After the merge, main has all the dark-mode work in it, and the album shows the story: a branch was created, work was done, and it was merged.
>
> Most of the time, the merge goes smoothly and I do it with one step.
>
> **Sometimes, though, there's a conflict.** A **conflict** happens when the exact same line of a file was changed in two different ways, once on main and once on the branch. Git doesn't know which version to keep, so it stops and asks. Imagine two people each rewriting the same sentence of the essay differently. A person has to pick. In our case, I'll look at both versions, explain the difference to you in plain English ("On main, the title is green. On the branch, it's dark blue."), and ask which one you want. Then I'll finish the merge. Conflicts sound dramatic, but they're normal and fixable.

### Deleting a branch

> **AI:** After a merge, the branch has done its job, so I tidy up by deleting it. That doesn't delete your work. The work is now safely inside main. It just removes the limb's name tag.
>
> If we decide a branch was a bad idea, I can delete it *without* merging. Then the whole experiment disappears, and main never knew about it.

Maya decided to try it. The AI created the `dark-mode` branch. An hour later, Maya looked at the result.

> **Maya:** I love it! Let's keep it.
>
> **AI:** Merging now... done. Dark mode is now part of main. I've deleted the old branch. Your album shows the whole story.

> **If I want to...** try a big or risky idea without endangering what already works,\
> **...I should ask the AI to:** "Make a branch called [name] and do this experiment there."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** your main project stays untouched. Your experiment lives in a separate copy. You can switch between the two anytime by asking.

> **If I want to...** keep an experiment that turned out great,\
> **...I should ask the AI to:** "Merge the [name] branch into main."
>
> **If I ask the AI to** merge,\
> **...then this will happen:** the new work is added to your main project. The AI will warn you if there are conflicts and will explain choices before deciding. After a merge, the main version of your site *will* look different, so check it.

> **If I want to...** throw away an experiment I didn't like,\
> **...I should ask the AI to:** "Delete the [name] branch without merging it."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** the experiment's changes are gone (it's hard to get them back afterward), and main stays exactly as it was.

> **If I want to...** work on two ideas at once, like a new menu and a new color scheme,\
> **...I should ask the AI to:** "Use a separate branch for each idea."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** each idea stays in its own box, so one can fail or succeed without affecting the other. Later you can merge them one at a time.

**A good habit:** whenever you say "I want to try something," the AI should offer a branch. Whenever you say "I'm sure about this, just do it," small changes can go straight on main.

## Chapter 8: Protecting Against a Disaster (Introducing GitHub)

On Monday, Maya's laptop fell off the couch. The screen flickered, and then it wouldn't turn on.

Fortunately, this was only a pretend scenario the AI had made up to teach her something. But it made her heart race.

> **Maya:** Wait. Where is my photo album stored?
>
> **AI:** On your laptop. In that hidden `.git` folder.
>
> **Maya:** So if my laptop dies...
>
> **AI:** ...the album dies with it. Every picture, every backup, gone. That's a real risk. Version control protects you from *mistakes*, but not from a dead computer, a stolen laptop, or a spilled drink.
>
> The fix is to keep a second copy of the album somewhere else, far from your laptop. That's where **GitHub** comes in.

### What is GitHub?

> **AI:** **GitHub** is a website where you can store a copy of your project and its whole photo album. It's like a big, safe storage locker in the sky. Think of Google Drive or iCloud, but built especially for projects like ours. It's free for what you need.
>
> A copy of your project stored on GitHub (or any other faraway place) is called a **remote**. "Remote" just means "somewhere else, not on this computer."
>
> GitHub does four jobs for you:
>
> 1. **Backup.** If your laptop explodes, your whole project and its history are safe.
> 2. **Sharing.** You can send someone a web link, and they can look at your project.
> 3. **Collaboration.** Other people can help improve your project, if you let them.
> 4. **Access from anywhere.** You can get your project onto any other computer.

### The one thing I can't do for you

> **AI:** I can do almost everything. But there's one thing I can't do: **create your GitHub account.** An account is a promise between a *person* and a company, and I can't make that promise for you. It needs your email address, your password, and your choices. So this is the one step you must do yourself. I'll walk you through it. It takes about ten minutes.

### Part A: Create your GitHub account

> **AI:** Follow these steps exactly.
>
> **Step 1. Open your web browser** (Chrome, Safari, Edge, or whatever you normally use) and go to the address **github.com**.
>
> **Step 2. Click the "Sign up" button.** It's near the top right corner of the page.
>
> **Step 3. Enter your email address.** Use an email you check often, because GitHub will send you messages. Then click the Continue button.
>
> **Step 4. Make up a password.** Pick a long one that's hard to guess. A good trick is to string together four random words, like *purple-teapot-staircase-moon*. Don't reuse a password from another website. If you have a password manager, let it create and save one for you.
>
> **Step 5. Pick a username.** This is your public name on GitHub, and it appears in the web address of your projects. For example, if you choose "maya-grows," your page will be github.com/maya-grows. Choose something you'd be comfortable showing a future employer. You can use letters, numbers, and dashes. If your first choice is taken, GitHub will tell you, and you can try another.
>
> **Step 6. Answer the questions.** GitHub may ask whether you'd like emails about product updates. You can say no. It may also ask you to solve a small puzzle to prove you're a human, like rotating a picture. That's normal.
>
> **Step 7. Check your email.** GitHub sends a short code (usually 6 or 8 digits). Type that code on the GitHub page. This proves that the email address is really yours.
>
> **Step 8. Choose the free plan.** If GitHub offers paid plans, pick the one that says **Free**. You don't need to pay anything.
>
> **Step 9. Turn on extra protection (strongly recommended).** Go to your account settings and look for **"Password and authentication."** Turn on **two-factor authentication**. That's a fancy name for a double lock. After you type your password, GitHub also asks for a code from an app on your phone. That way, even if a thief steals your password, they can't get in. GitHub will show you step-by-step instructions on screen. Write down the backup codes it gives you and store them somewhere safe, like a notebook in a drawer.
>
> **Step 10. Tell me your username.** When you're done, just type your GitHub username to me. I'll take it from there.

Maya followed along. Fifteen minutes later:

> **Maya:** Done! My username is maya-grows.
>
> **AI:** Wonderful! You now own a piece of the internet. Next, I need to prove to GitHub that I'm allowed to act for you.

### Part B: Let the AI connect to your account

> **AI:** Right now, GitHub doesn't know I exist. If I try to put your project there, it will say, "Who are you? I don't know you." So I need a *permission slip* from you that says, "Yes, this helper may use my account."
>
> I'll start the process. GitHub will show a short code. You then type that code on GitHub's website to approve me. It's like a secret handshake between the three of us.

The AI started the process and showed Maya a message:

> **AI:** I'm asking GitHub to let me in. It gave me a one-time code: **AB12-CD34**. Here's what you do:
>
> **Step 1.** Open your browser and go to **github.com/login/device**.
>
> **Step 2.** If GitHub asks you to sign in, sign in with the username and password you made. (If you turned on two-factor protection, it will ask for a code from your phone.)
>
> **Step 3.** Type the code I gave you, **AB12-CD34**, into the box. Use capital letters and the dash exactly as shown. (Your code will be different from the one in this story, so use the one I give you.)
>
> **Step 4.** Click the green **"Authorize"** button. GitHub will explain what permissions it's giving. You're allowing me to create and update projects on your behalf. This is expected, so it's okay to say yes.
>
> **Step 5.** Come back here and tell me when you've done it.

Maya typed the code and clicked the button.

> **Maya:** Okay, it says "Congratulations, you're all set!"
>
> **AI:** I can see that too. I'm connected! A reminder about safety, though. That permission slip lets me act as you on GitHub. Only approve this for tools you trust. If you ever want to cancel it, go to GitHub's settings, find "Applications," and remove it. I'll stop working immediately.

### Part C: Put Garden Buddy on GitHub

> **AI:** Now for the fun part. I'm going to create a home for Garden Buddy on GitHub. Before I do, there's a choice only you can make: **public or private?**
>
> A **public** project can be seen by anyone in the world. They can look at it and copy it, but they can't change *your* version unless you let them. This is great if you want a portfolio or want to share your work.
>
> A **private** project can only be seen by you and the people you invite. This is a good choice if the project is unfinished, personal, or you're unsure.
>
> You can change this later, so it's not a permanent choice.
>
> **Maya:** Private for now.
>
> **AI:** Good, that's safe. Here's what I'm doing:
>
> 1. I created a new, empty project on GitHub called **garden-buddy**.
> 2. I connected your laptop's project to it. In Git, we give the faraway copy a nickname, and the traditional nickname is **origin**. It just means, "the main faraway copy."
> 3. I **pushed** your project up to GitHub. To **push** means to send your saves from your laptop up to the faraway copy. It's like uploading photos to a cloud album. Every picture in your album, all of the history, goes up, not just the latest version.
>
> It's done! If you go to github.com/maya-grows/garden-buddy in your browser, you'll see all your files.

Maya looked. There was her project, in a web page, with a list of her files and the names of her saves.

> **Maya:** And my secret weather key? Is it up there?
>
> **AI:** I checked. It's not. Remember the ignore list? Git skipped it, so it never left your laptop. That's the ignore list doing its job.

> **If I want to...** back up my project so a broken laptop won't destroy it,\
> **...I should ask the AI to:** "Push my project to GitHub." (Or after the first time: "Back up my latest saves to GitHub.")
>
> **If I ask the AI to** push,\
> **...then this will happen:** the faraway copy on GitHub is updated to match your laptop. Nothing on your laptop changes. Anyone you've allowed can then see the newest version.
>
> **Remember:** a push only sends *saved* work (commits). If you have unsaved changes, they won't go up. Ask the AI to save first, then push.

## Chapter 9: Pushing, Pulling, and Starting Over on a New Computer

A week later, Maya's pretend disaster became real. Her laptop's hard drive failed. She bought a new one.

> **Maya:** I lost everything!
>
> **AI:** Take a breath. Did we push to GitHub?
>
> **Maya:** Yes, last night.
>
> **AI:** Then you've lost almost nothing. Here's how we get it all back.
>
> On your new laptop, we need two things: me (your AI partner) and access to your GitHub account. Once I'm set up and signed in, using the same steps as before, I'll **clone** your project.
>
> To **clone** means to make a complete copy of a project from GitHub onto your computer, including the entire photo album. It's called cloning because the copy is identical to the original, like a clone in a science-fiction movie.

The AI did it. Within a minute, Garden Buddy was back on her screen, with every save from the beginning.

> **AI:** Remember that anything we *didn't* put on GitHub is gone. That includes your secret weather key, because we kept it out on purpose. I'll help you get a fresh one from the weather company's website and set up a new `.env` file. That's the price of keeping secrets safe.

> **If I want to...** get my project onto a new computer,\
> **...I should ask the AI to:** "Clone my garden-buddy project from GitHub onto this computer."
>
> **If I ask the AI to** clone,\
> **...then this will happen:** a full copy of the project, with its whole history, appears on this computer. Your GitHub copy is untouched. Secrets and ignored files won't come with it, so we'll recreate those.

### Pulling

> **AI:** There's one more word: **pull**. To **pull** means to bring updates *from* GitHub *down* to your laptop. It's the opposite of a push.
>
> When would you need that? Suppose you worked on your project from your school's computer yesterday and pushed it. Today, on your home computer, your folder doesn't have yesterday's work yet. I'll *pull* the latest saves from GitHub, and your home computer catches up. It's like syncing.
>
> The same goes when a friend helps with your project. Their changes land on GitHub, and I pull them down to you.

> **If I want to...** get the latest work from GitHub onto this computer,\
> **...I should ask the AI to:** "Pull the newest changes from GitHub."
>
> **If I ask the AI to** pull,\
> **...then this will happen:** new saves from GitHub are added to your laptop's copy. If you've been editing the same lines, the AI may need to settle a conflict with you first.
>
> **A tip:** if you work from more than one computer, always pull *before* you start, and push *after* you finish. It's like checking the whiteboard before you start and updating it when you leave.

## Chapter 10: Letting Other People See and Help

Garden Buddy was getting good. Maya's friend Priya wanted to try it.

> **Maya:** Can I let Priya see my project?
>
> **AI:** Yes, and there are three levels. Let me explain each.

### Level 1: Just looking

> **AI:** If you make the project **public**, Priya can see it by visiting its web address, with no account needed. She can read it and download a copy. But she can't change *your* version.
>
> Before we make it public, I'll do a safety check. I'll scan your album for anything private: secret keys, personal phone numbers, anything embarrassing. Since the album keeps everything forever, anything we ever saved will be visible to the world. If I find something, we deal with it first.
>
> Public projects should also have two helpful files:
>
> A **README**. This is the front door. It's a file that appears on your project's GitHub page, and it explains what your project is, what it does, and how to use it. I'll write it for you in friendly language, and you can approve it.
>
> A **license**. This is a short legal note that says what others are allowed to do with your project. It could say, "Anyone may use and copy this, as long as they give me credit." Without a license, other people technically aren't allowed to reuse your work, even though they can see it. I'll explain the common options in plain language and let you pick. You don't need to read legal documents. I'll summarize them.

> **If I want to...** let anyone in the world see my project,\
> **...I should ask the AI to:** "Check my project for anything private, add a README and a license, then make it public."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** everyone can see all your files and your complete history. You can switch it back to private later, but anyone who copied it while it was public keeps their copy. So think carefully before going public.

### Level 2: Inviting someone as a helper

> **AI:** If Priya should be able to *change* your project, you can invite her as a **collaborator**. I can send the invitation if you give me her GitHub username. She'll get an email and must accept. Once she does, she can push changes directly.
>
> I suggest she works on a branch, not directly on main. That way you can look at her work before it joins the main version.

### Level 3: Suggestions from strangers

> **AI:** What if someone you *don't* know wants to improve your public project? They can't change your copy directly, which is a good thing. Instead, they make their own copy on GitHub, called a **fork**. Then they change *their* copy, and when they're happy, they send you a polite request that says, "I made a change. Would you like to add it to your project?" That request is called a **pull request**.
>
> You can think of it like a suggestion box. Strangers put a note in the box with their idea attached. You (or I, on your behalf) can read it, and then click one button to accept it or one to say no thanks. Nothing changes in your project until you say yes.
>
> The same idea works for friends. Priya could make a branch, and then open a pull request to ask, "Please merge my branch into main." You look it over first. This is the way most teams around the world work together.

> **If I want to...** control what changes join my project,\
> **...I should ask the AI to:** "Show me the pull request from Priya and explain in plain language what it changes."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** you get a summary only. Nothing in your project changes. When you approve, you can say, "Accept it," and the AI merges the changes into main.

> **If I want to...** help improve someone else's public project,\
> **...I should ask the AI to:** "Fork this project and suggest this improvement to the owner."
>
> **If I ask the AI to** do that,\
> **...then this will happen:** a copy appears under *your* account. Your changes go there, and a request goes to the owner. Their project is not changed unless *they* accept.

## Chapter 11: A Typical Week, Start to Finish

Months later, Maya had a rhythm. Here's what a normal working session looked like.

> **Monday, 4:00 PM.** Maya sits down at her computer.
>
> **Maya:** Good afternoon! Please pull the latest changes from GitHub, in case I did anything from another computer.
>
> **AI:** Pulled. You're up to date. What shall we work on?
>
> **Maya:** I want to add a "Plant of the Week" section. It's a big idea, and I'm not sure I'll like it.
>
> **AI:** That sounds like a good case for a branch. I'll call it `plant-of-the-week` and do the work there, so main stays safe.
>
> *(The AI works, saving after each small step, with clear labels.)*
>
> **Maya:** Hmm, I don't love the layout. Can you go back to how it looked before you added the picture?
>
> **AI:** Sure. I'll undo the last save on this branch. Done. The picture is gone, and the history remembers that we tried it.
>
> *(A few more changes follow.)*
>
> **Maya:** That's it! I love it!
>
> **AI:** Great! I'll merge it into main, delete the branch, and push to GitHub so it's backed up.
>
> **AI:** All done. Everything's backed up. Your album now has twelve new pictures, and your site has a new feature.

## Chapter 12: The Cheat Sheet

Maya's teacher asked her to make a one-page summary. Here it is. Keep this one handy.

### "I want to... so I ask the AI to..."

| If I want to... | I ask the AI to... |
|:---------------------------|:-------------------------------------------|
| Start keeping a history of my project | "Set up version control in this project." |
| Save my progress at a good moment | "Save my work with a clear label." |
| See what's changed since my last save | "Tell me what's changed since my last save." |
| See my project's history | "Show me the history in plain English." |
| Keep secrets and junk out of the album | "Make sure my secrets and clutter are on the ignore list." |
| Throw away my unsaved changes | "Discard everything since my last save." |
| Undo a change I already saved | "Undo the save called [name], but keep it in the history." |
| Peek at an old version | "Show me what the project looked like on [day]. Don't change anything." |
| Recover one old file | "Bring back the old version of [file]." |
| Try something risky safely | "Make a branch for this experiment." |
| Keep a successful experiment | "Merge that branch into main." |
| Abandon a failed experiment | "Delete that branch without merging." |
| Back up to the internet | "Push my project to GitHub." |
| Set up a second computer | "Clone my project from GitHub." |
| Get the latest from GitHub | "Pull the newest changes." |
| Let others look | "Check for private stuff, add a README and license, then make it public." |
| Let a friend help | "Invite [username] as a collaborator." |
| Review a suggestion | "Show me the pull request and explain it simply." |

### "I asked the AI to... so what will happen?"

| If I ask the AI to... | Then this happens to my project... |
|:---------------------------|:-------------------------------------------|
| Set up version control | A hidden `.git` folder appears. Nothing visible changes. |
| Commit (save) | A new snapshot is added. Your files stay the same. |
| Show history or status | You get a report only. Nothing changes. |
| Add something to the ignore list | Git stops tracking it. It stays on your computer but isn't saved or backed up. |
| Discard unsaved changes | Your files snap back to the last save. **The discarded work is gone for good.** |
| Revert a save | A new save reverses the old one. The old save stays in history. |
| Look at an old version | Files temporarily look old. You switch back when done. |
| Create a branch | A parallel copy for experiments. Main is untouched. |
| Merge a branch | The branch's work joins main. Your project changes. |
| Delete a branch without merging | The experiment is thrown away. |
| Push | GitHub gets your latest *saved* work. Your laptop is unchanged. |
| Pull | Your laptop gets the latest work from GitHub. |
| Clone | A complete copy appears on this computer. |
| Make the project public | Anyone can see everything, including old history. |

### The five golden rules

1. **Save often, with clear labels.** You'll thank yourself later.
2. **Never save secrets.** Keep passwords and keys on the ignore list from day one.
3. **Use a branch for any big or risky idea.** Main is for things that work.
4. **Push to GitHub at the end of every session.** It's your safety net.
5. **When in doubt, ask the AI to explain before it acts.** You can say, "Tell me what this will do first, in plain English." A good AI partner will always do that.

## Epilogue

Months later, Maya showed her little brother Garden Buddy. He asked her how she'd made it.

> **Maya:** I didn't write the code. My AI partner did. My job was to know what I wanted, to try bold ideas, and to say "undo that" when I changed my mind.
>
> **Brother:** What if the AI messes up?
>
> **Maya:** Then we go back to the last good picture. That's the best part. I'm never afraid to try something, because I know I can always get back to a time when things worked.

## Glossary (Every Strange Word, Explained Simply)

- **Version control:** a system that remembers every saved version of your project, so you can go back in time.
- **Git:** the free tool that does version control. Your AI runs it for you.
- **Repository (repo):** a project folder plus its photo album of saves.
- **Commit:** one saved snapshot of the whole project, with a label.
- **Commit message:** the short label describing what changed.
- **Staging area:** the "table" where files wait before being sealed into a commit.
- **Add:** choosing which changed files go into the next commit.
- **.gitignore:** a list of things Git should never save, such as secrets and clutter.
- **API key:** a secret password that lets your app use another company's service.
- **Revert:** undoing a saved change by adding a new save that reverses it.
- **Branch:** a parallel copy of your project for safe experiments.
- **Main:** the primary branch, the version you trust.
- **Merge:** combining a branch's work into another branch, usually main.
- **Conflict:** when the same line was changed two different ways and a person must choose.
- **GitHub:** a website that stores copies of projects and lets people share them.
- **Remote:** a copy of your project stored somewhere else, such as GitHub.
- **Origin:** the usual nickname for your main remote.
- **Push:** sending your saves from your computer to GitHub.
- **Pull:** bringing new saves from GitHub to your computer.
- **Clone:** making a full copy of a GitHub project on your computer.
- **Public / Private:** whether everyone can see a project, or only people you invite.
- **README:** the front-door page that explains your project.
- **License:** a note saying what others may do with your work.
- **Collaborator:** a person you've invited to change your project.
- **Fork:** your own copy of someone else's project on GitHub.
- **Pull request:** a polite request that says, "Please add my changes to your project."
- **Two-factor authentication:** a double lock on your account: a password plus a code from your phone.