# First-Day Setup Checklist — JavaFX Maven Project

Use this checklist **before you start working** on the project.  
If all items pass, your environment is correctly set up.

## Tech Stack
- Database: MongoDB Shared Cluster (Stubbed for now)
- Backend: Django (python)
- Frontend: React frameowrk with Typescript
---

## 1. Required Software

Confirm you have **all** of the following:

- ✅ **JDK 25** installed
- ✅ **IntelliJ IDEA** (Community or Ultimate)
- ✅ Git installed

> ⚠ **IntelliJ is the expected IDE for this course.**  
> Students using any other IDE may encounter setup and collaboration issues when working in groups that use IntelliJ exclusively.  
> If you use something other than IntelliJ, you are responsible for resolving any IDE-specific issues.

---

## 2. Clone the Repository

Clone the starter repository using Git (HTTPS or SSH):

```
git clone <repo-url>
cd <repo-directory>
```

Do not copy files manually between machines.

---

## 3. Open the Project in IntelliJ

1. Open IntelliJ IDEA
2. Choose Open
3. Select the root folder of the repository
4. When prompted:
    - Trust the project
    - Allow IntelliJ to import the Maven project

IntelliJ should detect this as a Maven project automatically.

---

## 4. Verify the JDK in IntelliJ

In IntelliJ:

1. File -> Project Structure -> Project
2. Confirm:
    - Project SDK: JDK 25
    - Language level: 25

If this is incorrect, fix it before continuing.

---

## 5. Do NOT Run MainApp Directly

Do not click the green Run button on MainApp.

Doing so will result in the following error:

```
JavaFX runtime components are missing
```

This project must be run using Maven, which correctly configures JavaFX.

---

## 6. Run the Project (Choose One Method)

### Option A - Run in IntelliJ (recommended)

1. Open the Maven tool window
2. Expand:
   Project
   -> Plugins
   -> javafx
3. Double-click:
   javafx:run

A JavaFX window should open.

---

### Option B - Run from the Terminal (Maven Wrapper)

This project uses the Maven Wrapper.
You do not need to install Maven.

Windows (PowerShell):

```
.\mvnw.cmd javafx:run
```

macOS or Linux:

```
./mvnw javafx:run
```

First run note:
The first run may take one to two minutes while dependencies download. This is normal.

---

## 7. Expected Result

If everything is correct:
- A JavaFX window opens
- No JavaFX runtime errors appear
- No additional setup is required

You are ready to start the project.

---

## 8. Common Problems (Quick Check)

If something goes wrong, check these first:

- Running MainApp directly instead of javafx:run
- Wrong JDK selected in IntelliJ
- Installing JavaFX manually
- Using mvn instead of mvnw or mvnw.cmd

If the JavaFX window opens, your setup is correct.

---

## Summary

If the project runs using javafx:run, your setup is correct and you may begin work.

