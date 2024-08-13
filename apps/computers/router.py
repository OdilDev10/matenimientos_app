from datetime import datetime
from fastapi import APIRouter, Depends
from apps.computers.dto.create_dto import CreateComputerDTO
from apps.dtos.pagination_dto import GetComputersDTO
from utils import response_error

# from apps.auth.controller import get_user_disabled_current
# from apps.users.schemas import SchemaEntityusers
from .controller import (
    all_computers,
    all_computers_export,
    all_computers_name_and_id,
    create_computers,
    destroy_computers,
    find_one_computers,
    reactive_computer,
    update_computers,
)
from .models import computers_Model


class ComputersRouter:
    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route(
            "/computers",
            self.get_computers,
            methods=["GET"],
            tags=["computers".upper()],
        )
        self.router.add_api_route(
            "/computers/export/{range_date_one}/{range_date_two}",
            self.get_computers_to_export,
            methods=["GET"],
            tags=["computers".upper()],
        )
        self.router.add_api_route(
            "/computers_name_id",
            self.get_computers_name_and_id,
            methods=["GET"],
            tags=["computers".upper()],
        )
        self.router.add_api_route(
            "/computers",
            self.post_computers,
            methods=["POST"],
            tags=["computers".upper()],
        )
        self.router.add_api_route(
            "/computers/{id}",
            self.get_computer,
            methods=["GET"],
            tags=["computers".upper()],
        )
        self.router.add_api_route(
            "/computers/{id}",
            self.put_computers,
            methods=["PUT"],
            tags=["computers".upper()],
        )
        self.router.add_api_route(
            "/computers_active/{id}",
            self.put_computers_reactive,
            methods=["PUT"],
            tags=["computers".upper()],
        )
        self.router.add_api_route(
            "/computers/{id}",
            self.delete_computers,
            methods=["DELETE"],
            tags=["computers".upper()],
        )

    async def get_computers(
        self,
        params: GetComputersDTO = Depends(),
    ):
        try:
            print("LLEGO")
            return all_computers(params)
        except Exception as error:
            response_error(error, "Router computers")

    async def get_computers_to_export(
        self, range_date_one: datetime, range_date_two: datetime
    ):
        try:
            return all_computers_export(range_date_one, range_date_two)
        except Exception as error:
            response_error(error, "Router computers")

    async def get_computers_name_and_id(self):
        try:
            return all_computers_name_and_id()
        except Exception as error:
            response_error(error, "Router computers")

    # async def post_computers(self, computers: CreateComputerDTO = Depends()):
    async def post_computers(self, computers: computers_Model):
        try:
            return create_computers(computers)
        except Exception as error:
            response_error(error, "Router computers")

    async def get_computer(self, id: str):
        try:
            return find_one_computers(id)
        except Exception as error:
            response_error(error, "Router computers")

    async def put_computers(self, id: str, computers: computers_Model):
        try:
            return update_computers(id, computers)
        except Exception as error:
            response_error(error, "Router computers")

    async def put_computers_reactive(self, id: str):
        try:
            return reactive_computer(id)
        except Exception as error:
            response_error(error, "Router computers")

    async def delete_computers(self, id: str):
        try:
            return destroy_computers(id)
        except Exception as error:
            response_error(error, "Router computers")


router_computers = ComputersRouter().router
