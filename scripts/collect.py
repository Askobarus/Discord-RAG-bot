#!/usr/bin/env python
"""Запуск сбора данных из Discord"""
import asyncio
from src.collector.ds_bot import DiscordCollector

if __name__ == "__main__":
    collector = DiscordCollector()
    asyncio.run(collector.collect())