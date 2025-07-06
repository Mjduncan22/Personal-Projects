package com.example.plannerapp.db

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "tasks")
data class Task(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val title: String,
    val date: String,
    val startTime: String,
    val endTime: String,
    val notes: String,
    val color: String,
    val repeatDays: String?,
    val repeatUntil: String
)

