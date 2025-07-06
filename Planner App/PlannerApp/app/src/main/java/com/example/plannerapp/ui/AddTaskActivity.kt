package com.example.plannerapp.ui

import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.os.Build
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.plannerapp.R
import com.example.plannerapp.db.Task
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*
import com.example.plannerapp.db.AppDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.time.LocalDate
import java.time.format.DateTimeFormatter



class AddTaskActivity : AppCompatActivity() {

    private lateinit var titleInput: EditText
    private lateinit var startTimeInput: EditText
    private lateinit var endTimeInput: EditText
    private lateinit var dateInput: EditText
    private lateinit var notesInput: EditText
    private lateinit var endDateInput: EditText
    private lateinit var colorSpinner: Spinner
    private lateinit var saveButton: Button
    private lateinit var cancelButton: Button

    private val calendar = Calendar.getInstance()
    private val timeFormatter = SimpleDateFormat("hh:mm a", Locale.US)
    private val dateFormatter = SimpleDateFormat("yyyy-MM-dd", Locale.US)

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.add_task)

        titleInput = findViewById(R.id.titleInput)
        startTimeInput = findViewById(R.id.startTimeInput)
        endTimeInput = findViewById(R.id.endTimeInput)
        dateInput = findViewById(R.id.dateInput)
        notesInput = findViewById(R.id.notesInput)
        endDateInput = findViewById(R.id.endDateInput)
        colorSpinner = findViewById(R.id.colorSpinner)
        saveButton = findViewById(R.id.saveButton)

        saveButton   = findViewById(R.id.saveButton)
        cancelButton = findViewById(R.id.cancelButton)

        setupTimePickers()
        setupDatePickers()
        setupColorSpinner()
        setupSaveButton()

        cancelButton.setOnClickListener {
            finish()
        }
    }

    private fun setupTimePickers() {
        startTimeInput.setOnClickListener { showTimePicker(startTimeInput) }
        endTimeInput.setOnClickListener { showTimePicker(endTimeInput) }
    }

    private fun showTimePicker(target: EditText) {
        val hour = calendar.get(Calendar.HOUR_OF_DAY)
        val minute = calendar.get(Calendar.MINUTE)
        val dialog = TimePickerDialog(this, { _, selectedHour, selectedMinute ->
            calendar.set(Calendar.HOUR_OF_DAY, selectedHour)
            calendar.set(Calendar.MINUTE, selectedMinute)
            target.setText(timeFormatter.format(calendar.time))
        }, hour, minute, false) // false = 12-hour format
        dialog.show()
    }

    private fun setupDatePickers() {
        dateInput.setOnClickListener { showDatePicker(dateInput) }
        endDateInput.setOnClickListener { showDatePicker(endDateInput) }
    }

    private fun showDatePicker(target: EditText) {
        val year = calendar.get(Calendar.YEAR)
        val month = calendar.get(Calendar.MONTH)
        val day = calendar.get(Calendar.DAY_OF_MONTH)
        val dialog = DatePickerDialog(this, { _, y, m, d ->
            calendar.set(y, m, d)
            target.setText(dateFormatter.format(calendar.time))
        }, year, month, day)
        dialog.show()
    }

    private fun setupColorSpinner() {
        val colors = listOf("Red", "Green", "Blue", "Yellow", "Orange")
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, colors)
        colorSpinner.adapter = adapter
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun generateRecurringTasks(
        originalTask: Task,
        repeatDays: List<String>,  // e.g. ["Monday", "Wednesday"]
        repeatUntilDate: LocalDate
    ): List<Task> {
        val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
        val dayOfWeekMap = mapOf(
            "Monday" to 1,
            "Tuesday" to 2,
            "Wednesday" to 3,
            "Thursday" to 4,
            "Friday" to 5,
            "Saturday" to 6,
            "Sunday" to 7
        )

        val startDate = LocalDate.parse(originalTask.date, formatter)
        val tasks = mutableListOf<Task>()

        var currentDate = startDate.plusDays(1) // start from day after original

        while (!currentDate.isAfter(repeatUntilDate)) {
            val currentDayValue = currentDate.dayOfWeek.value // 1=Mon,...7=Sun

            for (repeatDay in repeatDays) {
                val targetDay = dayOfWeekMap[repeatDay] ?: continue
                if (currentDayValue == targetDay) {
                    // Create a new task copy with updated date
                    val recurringTask = originalTask.copy(
                        id = 0, // Room will auto-generate new ID
                        date = currentDate.format(formatter)
                    )
                    tasks.add(recurringTask)
                }
            }
            currentDate = currentDate.plusDays(1)
        }
        return tasks
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun setupSaveButton() {
        saveButton.setOnClickListener {
            val title = titleInput.text.toString()
            val date = dateInput.text.toString()
            val startTime = startTimeInput.text.toString()
            val endTime = endTimeInput.text.toString()
            val notes = notesInput.text.toString()
            val color = colorSpinner.selectedItem.toString()

            // Suppose getRepeatDays() returns List<Int> with Calendar day constants, e.g. [2,4,6]
            val repeatDays = getRepeatDays()
            val repeatUntilString = endDateInput.text.toString()

            val task = Task(
                title = title,
                date = date,
                startTime = startTime,
                endTime = endTime,
                notes = notes,
                color = color,
                repeatDays = repeatDays.joinToString(","),
                repeatUntil = repeatUntilString
            )

            // Save original and recurring tasks on a background thread (coroutine)
            lifecycleScope.launch {
                val db = AppDatabase.getInstance(this@AddTaskActivity)
                val taskDao = db.taskDao()

                // Insert original task
                taskDao.insertTask(task)

                // Only generate recurring tasks if repeatDays is not empty and repeatUntil is valid
                if (repeatDays.isNotEmpty() && repeatUntilString.isNotEmpty()) {
                    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
                    val repeatUntilDate = LocalDate.parse(repeatUntilString, formatter)

                    val repeatDayInts = getRepeatDays()
                    val repeatDaysStrings = convertIntsToDayNames(repeatDayInts)

                    val recurringTasks = generateRecurringTasks(task, repeatDaysStrings, repeatUntilDate)
                    if (recurringTasks.isNotEmpty()) {
                        taskDao.insertTasks(recurringTasks)
                    }
                }

                withContext(Dispatchers.Main) {
                    Toast.makeText(this@AddTaskActivity, "Task saved", Toast.LENGTH_SHORT).show()
                    finish()  // close activity after save
                }
            }
        }
    }

    private fun convertIntsToDayNames(days: List<Int>): List<String> {
        val dayMap = mapOf(
            Calendar.MONDAY to "Monday",
            Calendar.TUESDAY to "Tuesday",
            Calendar.WEDNESDAY to "Wednesday",
            Calendar.THURSDAY to "Thursday",
            Calendar.FRIDAY to "Friday",
            Calendar.SATURDAY to "Saturday",
            Calendar.SUNDAY to "Sunday"
        )
        return days.mapNotNull { dayMap[it] }
    }

    private fun getRepeatDays(): List<Int> {
        val days = mutableListOf<Int>()
        val dayIds = listOf(
            R.id.checkbox_monday to Calendar.MONDAY,
            R.id.checkbox_tuesday to Calendar.TUESDAY,
            R.id.checkbox_wednesday to Calendar.WEDNESDAY,
            R.id.checkbox_thursday to Calendar.THURSDAY,
            R.id.checkbox_friday to Calendar.FRIDAY,
            R.id.checkbox_saturday to Calendar.SATURDAY,
            R.id.checkbox_sunday to Calendar.SUNDAY
        )
        for ((id, dayConst) in dayIds) {
            val box = findViewById<CheckBox>(id)
            if (box.isChecked) days.add(dayConst)
        }
        return days
    }
}
