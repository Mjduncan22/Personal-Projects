package com.example.plannerapp

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.floatingactionbutton.FloatingActionButton
import androidx.lifecycle.lifecycleScope
import com.example.plannerapp.R
import com.example.plannerapp.db.AppDatabase
import com.example.plannerapp.ui.AddTaskActivity
import com.example.plannerapp.ui.theme.TaskAdapter
import kotlinx.coroutines.launch
import android.app.DatePickerDialog
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale



class MainActivity : AppCompatActivity() {
    private lateinit var taskAdapter: TaskAdapter
    private lateinit var db: AppDatabase
    private var selectedDate: String = getTodayDate()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_main)

        db = AppDatabase.getInstance(this)
        val dateButton    = findViewById<Button>(R.id.dateButton)
        val recyclerView  = findViewById<RecyclerView>(R.id.taskList)
        val addButton     = findViewById<FloatingActionButton>(R.id.addButton)

        taskAdapter = TaskAdapter()
        recyclerView.adapter = taskAdapter
        recyclerView.layoutManager = LinearLayoutManager(this)

        dateButton.text = selectedDate
        dateButton.setOnClickListener { showDatePicker() }

        addButton.setOnClickListener {
            startActivity(Intent(this, AddTaskActivity::class.java)
                .putExtra("selectedDate", selectedDate))
        }

        loadTasksForDate(selectedDate)
    }

    private fun loadTasksForDate(date: String) {
        lifecycleScope.launch {
            val tasks = db.taskDao().getTasksByDate(date)
            taskAdapter.submitList(tasks)
        }
    }

    @SuppressLint("DefaultLocale")
    private fun showDatePicker() {
        val calendar = Calendar.getInstance()
        val parts = selectedDate.split("-").map { it.toInt() }
        calendar.set(parts[0], parts[1] - 1, parts[2]) // Month is 0-indexed

        val picker = DatePickerDialog(
            this,
            { _, year, month, day ->
                val newDate = String.format("%04d-%02d-%02d", year, month + 1, day)
                selectedDate = newDate
                findViewById<Button>(R.id.dateButton).text = newDate
                loadTasksForDate(newDate)
            },
            calendar.get(Calendar.YEAR),
            calendar.get(Calendar.MONTH),
            calendar.get(Calendar.DAY_OF_MONTH)
        )
        picker.show()
    }

    private fun getTodayDate(): String {
        val formatter = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
        return formatter.format(Date())
    }

    override fun onResume() {
        super.onResume()
        loadTasksForDate(selectedDate)
    }
}
