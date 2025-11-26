"""
Script to clean up duplicate email entries in cold_emails.json.
Keeps the most recent entry for each unique email address.
"""
import json
from datetime import datetime

def cleanup_duplicates():
    # Load the data
    with open("cold_emails.json", "r") as f:
        data = json.load(f)
    
    # Create backup
    backup_filename = f"cold_emails_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Backup created: {backup_filename}")
    
    # Group emails by recipient_email (case-insensitive)
    email_groups = {}
    for email in data["emails"]:
        email_addr = email["recipient_email"].lower()
        if email_addr not in email_groups:
            email_groups[email_addr] = []
        email_groups[email_addr].append(email)
    
    # For each group, keep the most recent and merge information
    deduplicated_emails = []
    duplicates_removed = 0
    
    for email_addr, emails in email_groups.items():
        if len(emails) == 1:
            # No duplicates, keep as is
            deduplicated_emails.append(emails[0])
        else:
            # Multiple entries - merge them
            duplicates_removed += len(emails) - 1
            print(f"\n🔍 Found {len(emails)} entries for {email_addr}")
            
            # Sort by last_updated to get the most recent
            emails.sort(key=lambda x: x.get("last_updated", ""), reverse=True)
            most_recent = emails[0].copy()
            
            # Merge follow-up dates from all entries
            all_follow_ups = set(most_recent.get("follow_up_dates", []))
            for email in emails[1:]:
                # Add date_sent from older entries as follow-ups
                if email.get("date_sent"):
                    all_follow_ups.add(email["date_sent"])
                # Merge follow-up dates
                all_follow_ups.update(email.get("follow_up_dates", []))
            
            most_recent["follow_up_dates"] = sorted(list(all_follow_ups))
            
            # Use the earliest date_sent
            earliest_date = min(e.get("date_sent", "9999-99-99") for e in emails if e.get("date_sent"))
            if earliest_date != "9999-99-99":
                most_recent["date_sent"] = earliest_date
            
            # Merge notes
            all_notes = []
            for email in emails:
                if email.get("notes"):
                    all_notes.append(email["notes"])
            if all_notes:
                most_recent["notes"] = "\n---\n".join(all_notes)
            
            # Use the most complete recipient_name
            best_name = max(emails, key=lambda x: len(x.get("recipient_name", "")))["recipient_name"]
            if best_name:
                most_recent["recipient_name"] = best_name
            
            # Use the most complete institution
            best_institution = max(emails, key=lambda x: len(x.get("institution", "")))["institution"]
            if best_institution:
                most_recent["institution"] = best_institution
            
            print(f"   ✅ Merged into 1 entry (ID: {most_recent['id']})")
            print(f"   📅 Date sent: {most_recent['date_sent']}")
            print(f"   🔄 Follow-ups: {len(most_recent['follow_up_dates'])}")
            
            deduplicated_emails.append(most_recent)
    
    # Update data
    data["emails"] = deduplicated_emails
    
    # Save cleaned data
    with open("cold_emails.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ Cleanup complete!")
    print(f"   Original entries: {len(email_groups) + duplicates_removed}")
    print(f"   Duplicates removed: {duplicates_removed}")
    print(f"   Final entries: {len(deduplicated_emails)}")
    print(f"{'='*60}")

if __name__ == "__main__":
    cleanup_duplicates()
