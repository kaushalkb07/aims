from django_cron import CronJobBase, Schedule
from autoupdatedb.models import StockMovement  # Adjust this based on your model

class UpdateStockMovementCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # Run every 1 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "autoupdatedb.update_stock_movement"

    def do(self):
        # Example task: Auto update stock movement
        stock_movements = StockMovement.objects.filter(updated=False)
        for stock in stock_movements:
            stock.updated = True
            stock.save()
        print("Stock Movement Updated Successfully.")
