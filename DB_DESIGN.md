# Database Design Document: VNR-ACE Backend

This document outlines the end-to-end database design, current implementation details, schemas, and further improvements needed for the VNR-ACE Backend platform.

## Overview
- **Database Engine**: PostgreSQL
- **ORM / Framework**: SQLAlchemy (v2.0+) with Alembic for migrations
- **Driver**: Asyncpg / psycopg2-binary
- **Base**: Declarative Base mapped to Python classes.

---

## 1. Current Database Models & Schema

### `roles`
Stores application user types (e.g., Admin, Student, TPO).
- `id` (Integer, Primary Key)
- `name` (String, Unique, Indexed)

### `users`
System authentication credentials and role assignments.
- `id` (Integer, Primary Key)
- `email` (String, Unique, Indexed, Not Null)
- `password` (String, Not Null - Hashed)
- `role_id` (Integer, Foreign Key to `roles.id`)
- **Relationships**: `role`
    
### `students`
Core student academic and personal profiles.
- `id` (Integer, Primary Key)
- `roll_no` (String, Unique, Indexed, Not Null)
- **Personal Info**: `full_name`, `gender`, `dob`, `email`, `mobile`
- **Academic Info**: `branch`, `cgpa`, `tenth_cgpa`, `inter_percent`, `active_backlogs`, `passive_backlogs`
- **Addressing Info**: `category`, `home_town`, `district`, `state`, `pincode`
- **Placement Specfic**: `minor_degree`, `intern_status` (Boolean)
- `created_at` (DateTime)

### `minor_degrees`
Stores the secondary/minor degrees that students pursue.
- `id` (Integer, Primary Key)
- `student_id` (Integer, Foreign Key to `students.id`)
- `minor_name` (String, Not Null)
- **Relationships**: `student`

### `companies`
Registered companies visiting for placements.
- `id` (Integer, Primary Key)
- `name` (String, Indexed, Not Null)
- `sector` (String)
- `created_at` (DateTime)

### `placements`
Records of successfully placed students.
- `id` (Integer, Primary Key)
- `student_id` (Integer, Foreign Key to `students.id`)
- `company_id` (Integer, Foreign Key to `companies.id`)
- `ctc_lpa` (Float, Indexed)
- `placement_date` (DateTime)
- `is_internship` (Boolean, default False)
- `created_at` (DateTime)
- **Relationships**: `student`, `company`

### `offers`
Represents the offers made to a student (multiple offers per student possible).
- `id` (Integer, Primary Key)
- `student_id` (Integer, Foreign Key to `students.id`)
- `company_id` (Integer, Foreign Key to `companies.id`)
- `ctc_lpa` (Float)
- `offer_number` (Integer)
- `created_at` (DateTime)
- **Relationships**: `student`, `company`

### `job_notifications`
Details regarding a job opening / visiting company criteria.
- `id` (Integer, Primary Key)
- `company_name` (String, Indexed, Not Null)
- `role` (String, Not Null)
- `description` (Text)
- **Eligibility Criteria**: `min_cgpa`, `min_tenth_cgpa`, `min_inter_percent`, `max_active_backlogs`, `max_passive_backlogs`, `allowed_branches` (JSON)
- `created_at` (DateTime)

### `company_prep_questions`
Preparation material, interview experiences, and questions for specific companies.
- `id` (Integer, Primary Key)
- `company_name` (String, Indexed, Not Null)
- `experiences` (JSONB)
- `questions` (JSONB)
- `created_at` (DateTime)

---

## 2. Further Improvements & Changes Needed

While the core models handle the primary functionalities well, some refactoring and optimization is required to make the schema more robust, prevent data anomalies, and maintain referential integrity.

### 1. Fix Missing Foreign Key References
- **Issue**: `job_notifications` and `company_prep_questions` use a plain string `company_name` instead of a foreign key reference to `companies.id`. This can lead to orphaned records, typos, or difficulties in cascaded updates.
- **Solution**: Replace `company_name` with `company_id = Column(Integer, ForeignKey("companies.id"))` and establish an ORM relationship.

### 2. Normalization Fixes
- **Issue**: `students.minor_degree` is a `String` column, but a separate `minor_degrees` table handles this as a 1-to-many relationship with `students`. Keeping both creates redundant data and synchronization issues.
- **Solution**: Remove the `minor_degree` column from `students` and rely entirely on the `minor_degrees` joined table, or just use the field in the student table instead.

### 3. User & Student Table Bridging
- **Issue**: `students` holds an `email` field but lacks a dedicated connection to `users`. Authentication occurs on `users`, but the system needs to inherently know which `User` maps to which `Student`.
- **Solution**: Add `user_id = Column(Integer, ForeignKey("users.id"), unique=True)` to the `Student` model, making it a 1-to-1 relationship.

### 4. Optimize Data Types using ENUMS
- **Issue**: Columns like `branch`, `gender`, `category`, and `sector` are plain strings. This invites typos and invalid entries.
- **Solution**: Implement PostgreSQL `ENUM` types for restricted domains (e.g., `Enum('CSE', 'IT', 'ECE', name='branch_types')`).

### 5. Proper Bidirectional ORM Relationships
- **Issue**: While `Placement` has `student = relationship("Student")`, the `Student` model doesn't have a `placements` back-reference.
- **Solution**: Add `back_populates` / `backref` across major relationships. For example, in `Student`, add `placements = relationship("Placement", back_populates="student")` to allow easy queries like `student.placements`.

### 6. Introduce "Updated At" Timestamps
- **Issue**: Most tables have `created_at`, but no `updated_at`.
- **Solution**: Add `updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())` base models or mixins to track when records are modified.

### 7. Constraints and Validations
- **Issue**: Duplicate `placements` mappings (same student placed in the same company twice) are technically possible under the current schema.
- **Solution**: Add `UniqueConstraint('student_id', 'company_id')` to the `placements` and `offers` tables where relevant. Add string length sizing to standard constraints.
