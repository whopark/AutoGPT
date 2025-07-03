import logging
from typing import Annotated, Dict, List

import fastapi
import httpx

from backend.server.utils import get_user_id

router = fastapi.APIRouter()
logger = logging.getLogger(__name__)


def _parse_info(info_str: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for item in info_str.split(";"):
        if not item:
            continue
        if "=" in item:
            key, value = item.split("=", 1)
            result[key] = value
        else:
            result[item] = ""
    return result


def _parse_vcf(content: str) -> List[Dict[str, object]]:
    variants: List[Dict[str, object]] = []
    header: List[str] = []
    for line in content.splitlines():
        if line.startswith("##"):
            continue
        if line.startswith("#"):
            header = line.lstrip("#").split("\t")
            continue
        if not line.strip():
            continue
        fields = line.split("\t")
        record = dict(zip(header, fields))
        info_fields = _parse_info(record.get("INFO", ""))
        record["INFO_PARSED"] = info_fields
        fmt = record.get("FORMAT", "").split(":")
        samples = fields[len(header) :]
        record["SAMPLES"] = [dict(zip(fmt, s.split(":"))) for s in samples if s]
        variants.append(record)
    return variants


async def _annotate_with_oncotator(content: str) -> str:
    url = (
        "https://portals.broadinstitute.org/oncotator/" "service/api/annotate/variants"
    )
    headers = {"Content-Type": "text/plain"}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, content=content, headers=headers)
            resp.raise_for_status()
            return resp.text
    except Exception as e:  # pragma: no cover - network operations
        logger.exception("Oncotator annotation failed: %s", e)
        raise fastapi.HTTPException(status_code=502, detail="Oncotator error")


@router.post("/annotate")
async def annotate_vcf(
    file: fastapi.UploadFile,
    user_id: Annotated[str, fastapi.Depends(get_user_id)],
) -> Dict[str, object]:
    content_bytes = await file.read()
    content = content_bytes.decode("utf-8")
    variants = _parse_vcf(content)
    annotation = await _annotate_with_oncotator(content)
    return {"variants": variants, "annotation": annotation}
