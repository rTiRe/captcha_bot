sudo touch db.sqlite
python -m alembic upgrade head
sudo cp bot.service /etc/systemd/system/bot.service
sudo systemctl daemon-reload
wait
sudo systemctl start bot.service
sudo systemctl status bot.service