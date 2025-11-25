# 🖍️ Real-Time Collaborative Sketchbook 🎨

A **Django + Fabric.js**-based real-time collaborative sketchbook where multiple users can draw together, share pages in a book, and track each user's contributions by color.  
Built for **students, teams, and creators** to sketch ideas visually — together!

---

## 🚀 Features

- 🔒 **User authentication** (only collaborators can access a sketch)
- 📚 **Book and sketch system** for organizing pages
- 🎨 **Unique color per user** in a sketchbook (auto-assigned)
- 🔁 **Real-time stroke syncing** (WebSockets-ready backend)
- 💾 **Strokes saved in database** (per sketch)
- 🧽 **Eraser tool** and **undo support** (with Fabric.js)
- 📸 **Export sketch as image**
- 🔍 **Per-user stroke tracking** for future OCR/AI features

---

## ⚙️ Tech Stack

**Backend**: Django + Django Auth  
**Frontend**: HTML + Fabric.js  
**Real-time**: Django Channels (WebSockets) *(planned)*  
**Database**: SQLite / PostgreSQL  
**Image Upload**: Django ImageField (`media/sketches/`)

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/collab-sketchbook.git
cd collab-sketchbook
