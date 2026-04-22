import random
import Schedule
import Activity
import Facilitator
import Room

class FitnessScorer:

    #NOTE: This is a temporary function. Feel free to overwrite, rename, anything, but this is what's currently being called in Genetic_Developer.evaluate(). Take in a schedule, return its fitness score.
    @staticmethod
    def score(schedule: Schedule) -> float:
        score = 0.0
        
        score += FitnessScorer.facilitator_overloaded(schedule)
        score += FitnessScorer.room_capacity(schedule)
        score += FitnessScorer.room_equipment(schedule)
        score += FitnessScorer.facilitator_doublebooked(schedule)
        score += FitnessScorer.activity_preferences(schedule)
        score += FitnessScorer.activity_specific_adjustments(schedule)

        return score
    
    def facilitator_overloaded(schedule: Schedule) -> float:
        facilitator_counts = {}
        for activity in schedule.activities:
            facilitator = activity.assigned_facilitator
            if facilitator not in facilitator_counts:
                facilitator_counts[facilitator] = 0
            facilitator_counts[facilitator] += 1
        
        overload_penalty = 0.0
        for facilitator, count in facilitator_counts.items():
            if count > 4:  # Assuming a facilitator can handle at most 4 activities
                overload_penalty -= .5
            elif count < 3 and facilitator.name != "Tyler":  # Tyler is the committee chair and has a lighter load
                overload_penalty -= .2
        
        return overload_penalty
    
    def activity_preferences(schedule: Schedule) -> float:
        preference_score = 0.0
        for activity in schedule.activities:
            if activity.assigned_facilitator in activity.preferred:
                preference_score += .5
            elif activity.assigned_facilitator in activity.other:
                preference_score += .2
            else:
                preference_score -= .1
        
        return preference_score

    def facilitator_doublebooked(schedule: Schedule) -> float:
        score = 0.0
        for time_slot, activities in schedule.schedule.items():
            slot_facilitators = {}
            for activity in activities:

                # Count facilitator assignments per time slot
                fac = activity.assigned_facilitator
                if fac not in slot_facilitators:
                    slot_facilitators[fac] = 0
                slot_facilitators[fac] += 1
            
            # Apply facilitator load scoring per time slot
            for fac, count in slot_facilitators.items():
                if count == 1:
                    score += 0.2  # Only 1 activity in this time slot
                elif count > 1:
                    score -= 0.2  # More than one activity at the same time
        
        return score
    
    def room_capacity(schedule: Schedule) -> float:
        capacity_score = 0.0
        for activity in schedule.activities:
            # Calculate UsedSpaceRate as enrollment / capacity
            used_space_rate = activity.enrollment / activity.assigned_room.capacity
            
            # Apply scoring based on UsedSpaceRate ranges
            if used_space_rate > 1.0:
                # Overbooking: room too small
                capacity_score -= 1.0
            elif used_space_rate >= 0.83:
                # 83-100%: Excellent fit
                capacity_score += 0.8
            elif used_space_rate >= 0.75:
                # 75-83%: Good fit
                capacity_score += 0.5
            elif used_space_rate >= 0.67:
                # 67-75%: Fair
                capacity_score += 0.2
            elif used_space_rate >= 0.50:
                # 50-67%: Wasteful
                capacity_score -= 0.3
            else:
                # <50%: Very wasteful
                capacity_score -= 0.6
        
        return capacity_score

    def room_equipment(schedule: Schedule) -> float:
        equipment_score = 0.0
        for activity in schedule.activities:
            needsMet = 0;
            if activity.need_lab:
                if activity.assigned_room.has_lab:
                    needsMet += 1
            else:
                needsMet += 1
            if activity.need_projector:
                if activity.assigned_room.has_projector:
                    needsMet += 1
            else:
                needsMet += 1

            if needsMet == 2:
                equipment_score += .2
            elif needsMet == 1:
                equipment_score -= .1
            else:
                equipment_score -= .3
        
        return equipment_score

    def activity_specific_adjustments(schedule: Schedule) -> float:
        """
        Scoring adjustments for SLA 101 and SLA 191 activity sections based on:
        - Time slot proximity between sections
        - Shared facilitators in consecutive time slots
        - Building locations (Roman/Beach)
        """
        score = 0.0
        
        # Create time slot to hour mapping for distance calculations
        time_slots = ["10am", "11am", "12pm", "1pm", "2pm", "3pm"]
        time_to_hour = {
            "10am": 10, "11am": 11, "12pm": 12,
            "1pm": 13, "2pm": 14, "3pm": 15
        }
        
        # Build dictionaries to find activities by name prefix
        sla101_activities = []
        sla191_activities = []
        
        for time_slot, activities in schedule.schedule.items():
            for activity in activities:
                if activity.name.startswith("SLA101"):
                    sla101_activities.append((activity, time_slot))
                elif activity.name.startswith("SLA191"):
                    sla191_activities.append((activity, time_slot))
        
        # Helper function to check if a room is in Roman or Beach building
        def is_roman_or_beach(room):
            room_name = room.name.lower()
            return "roman" in room_name or "beach" in room_name
        
        # Helper function to get time slot index
        def get_time_index(time_slot):
            return time_slots.index(time_slot) if time_slot in time_slots else -1
        
        # Helper function to calculate hour difference between two time slots
        def get_hour_difference(slot1, slot2):
            if slot1 not in time_to_hour or slot2 not in time_to_hour:
                return float('inf')
            return abs(time_to_hour[slot1] - time_to_hour[slot2])
        
        # SLA 101 specific rules
        if len(sla101_activities) == 2:
            act1, slot1 = sla101_activities[0]
            act2, slot2 = sla101_activities[1]
            hour_diff = get_hour_difference(slot1, slot2)
            
            if slot1 == slot2:
                # Both sections in same time slot: -0.5
                score -= 0.5
            elif hour_diff > 4:
                # Sections more than 4 hours apart: +0.5
                score += 0.5
        
        # SLA 191 specific rules
        if len(sla191_activities) == 2:
            act1, slot1 = sla191_activities[0]
            act2, slot2 = sla191_activities[1]
            hour_diff = get_hour_difference(slot1, slot2)
            
            if slot1 == slot2:
                # Both sections in same time slot: -0.5
                score -= 0.5
            elif hour_diff > 4:
                # Sections more than 4 hours apart: +0.5
                score += 0.5
        
        # Mixed SLA 191 and SLA 101 rules
        if len(sla191_activities) > 0 and len(sla101_activities) > 0:
            for sla191_act, sla191_slot in sla191_activities:
                for sla101_act, sla101_slot in sla101_activities:
                    slot1_idx = get_time_index(sla191_slot)
                    slot2_idx = get_time_index(sla101_slot)
                    
                    if slot1_idx == -1 or slot2_idx == -1:
                        continue
                    
                    slot_diff = abs(slot1_idx - slot2_idx)
                    hour_diff = get_hour_difference(sla191_slot, sla101_slot)
                    
                    if slot_diff == 1:
                        # Consecutive time slots: +0.5
                        score += 0.5
                        
                        # Check if one is in Roman or Beach, the other isn't: -0.4
                        sla191_in_rb = is_roman_or_beach(sla191_act.assigned_room)
                        sla101_in_rb = is_roman_or_beach(sla101_act.assigned_room)
                        
                        if sla191_in_rb != sla101_in_rb:
                            # One in Roman/Beach, the other isn't: -0.4
                            score -= 0.4
                    
                    elif hour_diff == 2:
                        # Separated by 1 hour (e.g., 10am & 12pm): +0.25
                        score += 0.25
                    
                    elif sla191_slot == sla101_slot:
                        # Same time slot: -0.25
                        score -= 0.25
        
        return score