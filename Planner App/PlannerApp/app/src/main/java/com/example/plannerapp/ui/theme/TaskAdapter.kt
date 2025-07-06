package com.example.plannerapp.ui.theme

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.plannerapp.R
import com.example.plannerapp.db.Task

class TaskAdapter : ListAdapter<Task, TaskAdapter.TaskViewHolder>(TaskDiffCallback()) {

    inner class TaskViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val titleTv = itemView.findViewById<TextView>(R.id.taskTitle)
        private val timeTv  = itemView.findViewById<TextView>(R.id.taskTime)
        private val notesTv = itemView.findViewById<TextView>(R.id.taskNotes)

        fun bind(task: Task) {
            // 1) Text fields
            titleTv.text = task.title
            timeTv.text  = task.startTime ?: ""
            notesTv.text = task.notes ?: ""

            // 2) Background color
            val bgColor = mapTaskColor(task.color ?: "", itemView.context)
            itemView.setBackgroundColor(bgColor)
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): TaskViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        val view = inflater.inflate(R.layout.item_task, parent, false)
        return TaskViewHolder(view)
    }

    override fun onBindViewHolder(holder: TaskViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class TaskDiffCallback : DiffUtil.ItemCallback<Task>() {
        override fun areItemsTheSame(oldItem: Task, newItem: Task) =
            oldItem.id == newItem.id

        override fun areContentsTheSame(oldItem: Task, newItem: Task) =
            oldItem == newItem
    }

    private fun mapTaskColor(name: String, context: Context): Int =
        when (name) {
            "Red"    -> ContextCompat.getColor(context, R.color.taskRed)
            "Green"  -> ContextCompat.getColor(context, R.color.taskGreen)
            "Blue"   -> ContextCompat.getColor(context, R.color.taskBlue)
            "Yellow" -> ContextCompat.getColor(context, R.color.taskYellow)
            "Orange" -> ContextCompat.getColor(context, R.color.taskOrange)
            else     -> ContextCompat.getColor(context, android.R.color.darker_gray)
        }
}
