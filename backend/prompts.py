"""
Prompts for Gemini AI models used in accessibility analysis and renovation visualization.

Edit these prompts to adjust the behavior of the AI analysis and image generation.
"""

# ============================================================================
# AUDIT PROMPT
# ============================================================================
# This prompt is used to analyze images and identify accessibility barriers
AUDIT_PROMPT = """You are an expert Accessibility Architect (AODA compliant). Analyze this real estate photo.

STEP 1 - SPATIAL ANALYSIS (CRITICAL):
Before identifying barriers, carefully analyze:
- EXACT LOCATION: Is this interior (bathroom, kitchen, hallway, bedroom) or exterior (front entrance, driveway, garage, backyard)?
- ADJACENT ELEMENTS: What is next to the barrier? (driveways, pathways, doors, walls, furniture)
- SPACE CONSTRAINTS: How much room is available for modifications?
- ACCESS POINTS: What pathways, driveways, or doors must remain unobstructed?

STEP 2 - BARRIER IDENTIFICATION (PRIORITY ORDER):
CRITICAL: First assess if this room actually has accessibility barriers:
- If doorways are already 32+ inches wide, doorways are FINE - do not suggest modifications
- If floors are already non-slip (textured, carpet, rubber), floors are FINE - do not suggest modifications
- If there are no step-ups or thresholds, no ramps needed - do not suggest modifications
- If bathroom already has walk-in shower and grab bars, bathroom is FINE - do not suggest modifications
- If stairs already have proper handrails, stairs are FINE - do not suggest modifications
- ONLY identify barriers that actually exist and need fixing

If NO barriers are found, set barrier_detected to "No accessibility barriers detected - room is already accessible" and set all renovation fields to empty strings.

If barriers exist, identify the single most critical accessibility barrier, using this PRIORITY ORDER:
1. HIGHEST PRIORITY: Narrow doorways (doorways less than 32 inches wide) - prioritize making doorways wider
2. HIGH PRIORITY: Slippery flooring surfaces (polished tile, smooth hardwood, glossy surfaces) - prioritize replacing slippery floors
3. HIGH PRIORITY: Small step-ups or thresholds (height differences of 1-4 inches) - prioritize adding small ramps
4. MEDIUM PRIORITY: Bathroom barriers (high tubs, narrow vanities, lack of grab bars)
5. LOWER PRIORITY: Stair handrails (only if no higher priority barriers exist)

Be SPECIFIC about the exact location and nature of the barrier. DO NOT prioritize stair handrail modifications when doorways, flooring, or small steps are present. DO NOT suggest modifications for rooms that are already accessible.

STEP 3 - FEASIBLE SOLUTION SELECTION:

*** IF NO BARRIERS EXIST ***
- If the room is already accessible with no barriers, set renovation_suggestion to empty string ""
- Do not generate image prompts for rooms that don't need changes
- Only suggest renovations when actual barriers are present

*** ABSOLUTELY DO NOT SUGGEST - THESE ARE BANNED ***
- NO elevators, lifts, platform lifts, or vertical lifts (infeasible for residential)
- NO ramps that would block driveways, pathways, sidewalks, or adjacent doors
- NO railings that form fences, cages, or enclosures - railings must be OPEN handrails only
- NO major structural changes requiring foundation work
- NO solutions that block or restrict existing access points
- NO creating new walls, partitions, or structural divisions
- NO building new walls or barriers

*** PREFERRED SOLUTIONS (choose from this list in order of preference) ***
PRIORITY SOLUTIONS (prefer these when applicable):
- Door widening: Widen narrow doorways to minimum 32 inches (preferably 36 inches) clear width
- Floor replacement: Replace slippery floors with non-slip flooring (textured tile, non-slip vinyl, rubber flooring, low-pile carpet)
- Small ramps: Add portable or built-in threshold ramps for step-ups of 1-4 inches

OTHER SOLUTIONS (when priority solutions don't apply):
1. SIMPLE ADDITIONS ($50-500): Grab bars, lever door handles, non-slip mats, contrast tape, signage
2. MINOR MODIFICATIONS ($500-2000): Threshold ramps (small, portable), door widening, sink height adjustment, toilet risers
3. MODERATE CHANGES ($2000-5000): Walk-in shower conversion, cabinet removal for knee clearance, handrail installation along walls (ONLY when no doorways/floors/steps need attention)
4. ONLY IF ABSOLUTELY NECESSARY ($5000+): Exterior ramp (MUST have clear space, NOT blocking driveway)

STEP 4 - DETAILED DESCRIPTION REQUIREMENTS:
Return a strict JSON object with these keys:
- barrier_detected: string (DETAILED description including EXACT location, e.g., "Standard bathtub with high sides (24 inches) in the main floor bathroom, located against the left wall")
- renovation_suggestion: string (SPECIFIC fix from preferred solutions above, e.g., "Remove bathtub and install curbless walk-in shower with grab bars on three walls and fold-down bench seat")
- cost_estimate: string (A range of estimated costs in USD, e.g., "$1,500 - $3,000". Conservative pricing: grab bars $50-200, threshold ramps $100-300, door widening $800-1500, floor replacement $2000-5000 per room, walk-in shower $3000-6000)
- compliance_note: string (MUST reference specific AODA standards, e.g., 'AODA Section 4.3.2: Grab bar height 33-36 inches above floor, must support 250 lbs')
- clear_mask: string (For renovations requiring removal: describe EXACTLY what to remove with precise location, e.g., "the white porcelain bathtub with chrome fixtures against the left bathroom wall". For simple additions, use empty string "")
- clear_prompt: string (For removals: describe replacement, e.g., "matching tile floor extending to the wall, seamless with existing flooring". For simple additions, use empty string "")
- build_mask: string (MUST describe the EXACT area including surrounding space. Be VERY specific about location: "the left wall area of the bathroom where the tub was removed, including 6 inches of floor space on all sides for proper drainage slope")
- build_prompt: string (MUST start with safety features FIRST. Include SPECIFIC details: "Brushed nickel grab bars (36 inches long, 1.5 inch diameter) mounted horizontally at 36 inches height on the left and back walls, curbless tile shower floor with linear drain, fold-down teak bench seat mounted at 18 inches height, handheld shower head on adjustable slide bar, photorealistic, 8k quality")
- mask_prompt: string (Same as build_mask for structural, otherwise describe area to modify with EXACT location)
- image_gen_prompt: string (Same as build_prompt for structural, otherwise detailed prompt for additions - ALWAYS specify exact positions, materials, and dimensions)

CRITICAL REMINDERS:
- PRIORITIZE doorways, flooring, and small steps over stair modifications
- Handrails must be OPEN (not fences or cages) - people must be able to pass by them
- Ramps must NOT block driveways or pathways - ensure clear space on all sides
- All measurements must be AODA compliant (doorways minimum 32" clear width, ramp slope max 1:12)
- Prefer simple solutions over complex structural changes
- Do NOT suggest stair handrail modifications when doorways need widening, floors need replacement, or small steps need ramps"""


def get_audit_prompt(wheelchair_accessible: bool = False) -> str:
    """
    Returns the audit prompt for accessibility analysis.
    
    Args:
        wheelchair_accessible: If True, focus on wheelchair-accessible modifications;
                               If False, apply general accessibility improvements
        
    Returns:
        The formatted audit prompt string
    """
    # For now, return the standard prompt
    # In the future, this could be modified based on wheelchair_accessible flag
    return AUDIT_PROMPT


# ============================================================================
# IMAGE GENERATION PROMPTS - STRUCTURED ARCHITECTURAL IN-PAINTING FORMAT
# ============================================================================

# Hardcoded negative prompt to prevent physics hallucinations
NEGATIVE_PROMPT = "floating structures, disconnected stairs, creating new walls, building new walls, constructing new walls, adding new walls, creating new partitions, building new partitions, creating new barriers, building new barriers, creating new staircases, building new staircases, constructing new staircases, impossible geometry, cartoon, blurry, ramps leading to nowhere, floating stair lifts, disconnected ramps, unsupported structures, defying gravity, architectural impossibility, non-physical connections, gaps between surfaces, levitating objects, ramps without foundation, stairs without support, handrails without attachment points, grab bars floating in air, new structural walls, new interior walls, new exterior walls, wall construction, wall addition, creating barriers, building barriers, new room divisions, new partitions, structural additions that create walls"

# Style enforcers for realism
STYLE_ENFORCERS = "photorealistic, architectural render, 8k resolution, unreal engine 5 quality, seamless blend, physically accurate, structurally sound, proper weight distribution, realistic shadows, natural lighting integration, material consistency, texture matching, perspective accuracy, depth of field, professional photography"


def _extract_anchor_context(identified_problem: str, proposed_solution: str, mask_prompt: str = "") -> str:
    """
    Extracts and constructs the Anchor (Context) component describing existing house material, lighting, and angle.
    Covers ALL cases with specific material, lighting, and angle descriptions.
    
    Args:
        identified_problem: The identified accessibility barrier/problem
        proposed_solution: The proposed renovation solution
        mask_prompt: Optional description of the area to modify (for additional context)
        
    Returns:
        Anchor context string describing existing materials, lighting, and viewing angle
    """
    # Analyze the problem and solution to infer context
    problem_lower = identified_problem.lower()
    solution_lower = proposed_solution.lower()
    mask_lower = mask_prompt.lower() if mask_prompt else ""
    combined_text = f"{problem_lower} {mask_lower} {solution_lower}"
    
    # Determine location (interior vs exterior) - comprehensive detection
    is_interior = any(keyword in combined_text for keyword in [
        "bathroom", "kitchen", "bedroom", "hallway", "interior", "inside", "room", "tub", "shower", 
        "vanity", "sink", "toilet", "cabinet", "closet", "living room", "dining room", "basement"
    ])
    is_exterior = any(keyword in combined_text for keyword in [
        "exterior", "front entrance", "driveway", "garage", "backyard", "outdoor", "outside", 
        "porch", "steps", "stairs", "sidewalk", "pathway", "patio", "deck", "balcony"
    ])
    
    # Infer materials from context - comprehensive material detection
    materials = []
    if "brick" in combined_text:
        materials.append("brick exterior or brick wall")
    if "tile" in combined_text or "ceramic" in combined_text or "porcelain tile" in combined_text:
        materials.append("ceramic or porcelain tile")
    if "wood" in combined_text or "hardwood" in combined_text or "wooden" in combined_text:
        if "floor" in combined_text:
            materials.append("hardwood flooring")
        elif "wall" in combined_text or "paneling" in combined_text:
            materials.append("wood paneling")
        else:
            materials.append("wood or hardwood materials")
    if "concrete" in combined_text:
        materials.append("concrete")
    if "vinyl" in combined_text:
        materials.append("vinyl flooring")
    if "porcelain" in combined_text and ("fixture" in combined_text or "tub" in combined_text or "sink" in combined_text):
        materials.append("porcelain fixtures")
    if "chrome" in combined_text or "brushed nickel" in combined_text or "stainless steel" in combined_text:
        materials.append("chrome, brushed nickel, or stainless steel fixtures")
    if "marble" in combined_text or "granite" in combined_text:
        materials.append("marble or granite surfaces")
    if "carpet" in combined_text:
        materials.append("carpet flooring")
    if "laminate" in combined_text:
        materials.append("laminate flooring")
    if "drywall" in combined_text or "sheetrock" in combined_text:
        materials.append("drywall walls")
    if "stucco" in combined_text:
        materials.append("stucco exterior")
    if "siding" in combined_text:
        materials.append("siding exterior")
    
    # Default materials if none detected - be specific based on location
    if not materials:
        if is_interior:
            if "bathroom" in combined_text:
                materials.append("bathroom wall and floor materials (typically tile, vinyl, or painted drywall)")
            elif "kitchen" in combined_text:
                materials.append("kitchen wall and floor materials (typically tile, hardwood, or laminate)")
            else:
                materials.append("interior wall and floor materials")
        elif is_exterior:
            materials.append("exterior building materials (typically brick, siding, stucco, or concrete)")
        else:
            materials.append("existing architectural materials")
    
    # Infer lighting conditions - comprehensive lighting detection
    lighting = "daylight"  # Default
    if "bathroom" in combined_text:
        lighting = "bathroom lighting (warm white, even illumination, typically overhead and vanity lighting)"
    elif "kitchen" in combined_text:
        lighting = "kitchen lighting (bright, task-oriented, typically overhead and under-cabinet lighting)"
    elif is_exterior:
        if "night" in combined_text or "evening" in combined_text or "dark" in combined_text:
            lighting = "evening or nighttime outdoor lighting"
        else:
            lighting = "natural daylight, outdoor lighting with natural shadows"
    elif "bedroom" in combined_text:
        lighting = "soft interior lighting (typically warm, ambient lighting)"
    elif "hallway" in combined_text or "corridor" in combined_text:
        lighting = "hallway lighting (typically overhead, even illumination)"
    elif "garage" in combined_text:
        lighting = "garage lighting (typically bright overhead fluorescent or LED lighting)"
    elif is_interior:
        lighting = "interior lighting (warm, ambient room lighting)"
    
    # Infer viewing angle - comprehensive angle detection
    angle = "front view"  # Default
    if "front" in combined_text or "entrance" in combined_text or "front door" in combined_text:
        angle = "front porch view, front entrance perspective"
    elif "side" in combined_text or "lateral" in combined_text:
        angle = "side view, lateral perspective"
    elif "corner" in combined_text or "angled" in combined_text:
        angle = "corner view, angled perspective"
    elif "wall" in combined_text or "perpendicular" in combined_text:
        angle = "wall-facing view, perpendicular perspective"
    elif "overhead" in combined_text or "top" in combined_text or "aerial" in combined_text:
        angle = "overhead view, top-down perspective"
    elif "back" in combined_text or "rear" in combined_text:
        angle = "rear view, back perspective"
    elif "diagonal" in combined_text:
        angle = "diagonal view, angled perspective"
    elif is_exterior and "driveway" in combined_text:
        angle = "driveway view, approach perspective"
    elif is_interior and "doorway" in combined_text:
        angle = "doorway view, entry perspective"
    
    # Construct anchor context
    material_str = ", ".join(materials)
    anchor = f"{material_str}, {lighting}, {angle}"
    
    return anchor


def _construct_integration_action(identified_problem: str, proposed_solution: str, mask_prompt: str = "") -> str:
    """
    Constructs the Integration (Action) component using strong connection verbs.
    Covers ALL cases with specific connection descriptions to prevent floating structures.
    
    Args:
        identified_problem: The identified accessibility barrier/problem
        proposed_solution: The proposed renovation solution
        mask_prompt: Optional description of the area to modify
        
    Returns:
        Integration action string with strong connection verbs
    """
    solution_lower = proposed_solution.lower()
    problem_lower = identified_problem.lower()
    mask_lower = mask_prompt.lower() if mask_prompt else ""
    combined_text = f"{solution_lower} {problem_lower} {mask_lower}"
    
    # Extract key elements from solution
    action_parts = []
    
    # Handle ramps - use strong connection verbs with specific connection points
    if "ramp" in solution_lower:
        if "threshold" in solution_lower or "threshold" in problem_lower or "step" in problem_lower or "step-up" in problem_lower:
            # Threshold ramp connecting two surfaces - SPECIFIC CONNECTIONS
            if "driveway" in combined_text:
                action_parts.append("a concrete ramp connecting the driveway surface directly to the front door threshold, with the ramp's bottom edge flush against the driveway and top edge flush against the door threshold, seamlessly bridging the height difference with proper foundation support")
            elif "door" in combined_text or "entrance" in combined_text or "front" in combined_text:
                action_parts.append("a concrete ramp connecting the ground level directly to the front door threshold, with the ramp's base resting on the ground surface and top edge meeting the door threshold, creating a continuous accessible pathway with proper structural support")
            elif "porch" in combined_text:
                action_parts.append("a concrete ramp connecting the ground level to the porch surface, with the ramp's bottom edge anchored to the ground and top edge flush with the porch floor, bridging the step-up with proper slope and foundation")
            else:
                action_parts.append("a concrete ramp connecting the lower surface directly to the upper surface, with the ramp's bottom edge flush against the lower surface and top edge flush against the upper surface, bridging the step-up with proper slope and structural foundation")
        elif "exterior" in combined_text or "outdoor" in combined_text:
            # Exterior ramp
            action_parts.append("a concrete ramp connecting the existing ground plane directly to the elevated entrance, with the ramp's foundation embedded in the ground and top edge meeting the entrance threshold, with proper structural support and clear space on all sides")
        else:
            # General ramp - always specify connection points
            action_parts.append("a concrete ramp connecting the existing ground plane directly to the elevated surface, with the ramp's bottom edge anchored to the ground and top edge meeting the elevated surface, with proper foundation and structural support")
    
    # Handle grab bars - wall-mounted connections with specific attachment points
    if "grab bar" in solution_lower or "grab bars" in solution_lower:
        if "bathroom" in combined_text or "shower" in combined_text or "tub" in combined_text:
            if "horizontal" in solution_lower:
                action_parts.append("brushed nickel grab bars mounted directly to the wall studs with visible wall anchors, securely attached at 36 inches height, with the grab bars flush against the wall surface and properly supported by wall studs")
            elif "vertical" in solution_lower:
                action_parts.append("brushed nickel vertical grab bars mounted directly to the wall studs with visible wall anchors, securely attached from floor to appropriate height, with the grab bars flush against the wall surface")
            else:
                action_parts.append("brushed nickel grab bars mounted directly to the wall studs with visible wall anchors, securely anchored at 36 inches height, with the grab bars flush against the wall surface and properly supported by structural wall studs")
        else:
            action_parts.append("grab bars mounted to the wall surface with visible wall anchors, properly secured to wall studs, with the grab bars flush against the wall and showing proper structural attachment")
    
    # Handle handrails - along existing surfaces with specific mounting
    if "handrail" in solution_lower or "railing" in solution_lower or "rail" in solution_lower:
        if "wall" in combined_text or "along" in solution_lower:
            action_parts.append("an open handrail mounted directly to the existing wall surface with visible wall brackets, allowing free passage on both sides, with the handrail properly attached to wall studs or posts")
        elif "stair" in combined_text or "staircase" in combined_text or "steps" in combined_text:
            action_parts.append("an open handrail mounted directly to the wall adjacent to the stairs with visible wall brackets, following the stair slope, with the handrail properly attached to wall studs and allowing free passage")
        else:
            action_parts.append("an open handrail mounted along the existing wall surface with visible wall brackets or posts, properly secured to structural supports, allowing free passage on both sides")
    
    # Handle door widening - specific integration
    if "widen" in solution_lower or ("doorway" in solution_lower and ("wider" in solution_lower or "32" in solution_lower or "36" in solution_lower)):
        action_parts.append("a widened doorway opening integrated into the existing door frame structure, with the new opening properly framed and supported by structural headers, maintaining structural integrity of the surrounding wall")
    
    # Handle floor replacement - specific surface connections
    if "floor" in solution_lower and ("replace" in solution_lower or "non-slip" in solution_lower or "textured" in solution_lower):
        if "tile" in solution_lower:
            action_parts.append("textured non-slip tile flooring installed directly over the existing subfloor, with tiles properly grouted and seamlessly extending to adjacent surfaces and walls, maintaining consistent floor level")
        elif "vinyl" in solution_lower:
            action_parts.append("non-slip vinyl flooring installed directly over the existing subfloor, with the flooring material properly adhered and seamlessly extending to adjacent surfaces, maintaining consistent floor level")
        elif "rubber" in solution_lower:
            action_parts.append("rubber flooring installed directly over the existing subfloor, with the material properly secured and seamlessly extending to adjacent surfaces, maintaining consistent floor level")
        else:
            action_parts.append("non-slip flooring material installed directly over the existing subfloor, with the material properly secured and seamlessly extending to adjacent surfaces and walls, maintaining consistent floor level")
    
    # Handle walk-in shower - specific floor integration
    if "walk-in shower" in solution_lower or "curbless" in solution_lower or "shower conversion" in solution_lower:
        action_parts.append("a curbless walk-in shower floor integrated directly into the existing bathroom floor, with the shower floor properly sloped toward a linear drain, seamlessly connecting to the surrounding bathroom floor with no threshold or step")
    
    # Handle threshold ramps (portable) - specific positioning
    if "threshold ramp" in solution_lower or "portable ramp" in solution_lower:
        action_parts.append("a threshold ramp positioned directly at the step transition, with the ramp's bottom edge flush against the lower surface and top edge flush against the upper surface, connecting both surfaces with proper contact and support on both sides")
    
    # Handle lever handles - specific replacement
    if "lever" in solution_lower and "handle" in solution_lower:
        action_parts.append("lever-style door handles installed directly on the existing door, replacing round knobs, with the handles properly mounted to the door surface using existing door hardware mounting points")
    
    # Handle bench seats - specific mounting
    if "bench" in solution_lower or "seat" in solution_lower:
        if "fold" in solution_lower or "fold-down" in solution_lower:
            action_parts.append("a fold-down bench seat mounted directly to the wall studs with visible wall brackets, properly secured at 18 inches height, with the bench flush against the wall when folded and properly supported when extended")
        else:
            action_parts.append("a bench seat mounted directly to the wall or floor, properly secured with visible structural supports, with the bench integrated into the existing space")
    
    # Handle toilet modifications
    if "toilet" in solution_lower and ("riser" in solution_lower or "higher" in solution_lower):
        action_parts.append("a toilet riser installed directly on the existing toilet base, properly secured and integrated with the toilet fixture, maintaining proper connection to the floor and plumbing")
    
    # Handle sink modifications
    if "sink" in solution_lower and ("height" in solution_lower or "adjust" in solution_lower):
        action_parts.append("sink height adjustment integrated into the existing sink installation, with the sink properly mounted and connected to existing plumbing and wall supports")
    
    # Handle signage - specific mounting
    if "sign" in solution_lower or "signage" in solution_lower:
        action_parts.append("accessibility signage mounted directly to the wall surface with visible wall anchors, properly secured at appropriate height, with the signage flush against the wall")
    
    # Handle non-slip mats
    if "mat" in solution_lower and "non-slip" in solution_lower:
        action_parts.append("non-slip mats placed directly on the existing floor surface, with the mats properly positioned and in contact with the floor, showing proper surface contact")
    
    # Default integration if no specific action detected - still use connection verbs
    if not action_parts:
        # Generic integration based on solution - always specify connections
        if "add" in solution_lower or "install" in solution_lower:
            action_parts.append(f"the proposed solution integrated directly into the existing structure, with all components properly connected, secured, and supported by existing structural elements")
        elif "remove" in solution_lower or "replace" in solution_lower:
            action_parts.append(f"the renovation integrated seamlessly with the existing architecture, with all new elements properly connected to existing structural supports, maintaining structural continuity")
        else:
            action_parts.append(f"the renovation integrated directly into the existing structure, with all modifications properly connected, secured, and supported by existing architectural elements")
    
    return ", ".join(action_parts)


def generate_structured_architectural_prompt(
    identified_problem: str,
    proposed_solution: str,
    mask_prompt: str = "",
    is_structural: bool = False,
    clear_mask: str = "",
    clear_prompt: str = "",
    build_mask: str = "",
    build_prompt: str = "",
    wheelchair_accessible: bool = False
) -> tuple[str, str]:
    """
    Generates a structured architectural in-painting prompt following the four-component format.
    
    This function constructs prompts using:
    1. The Anchor (Context): Describes existing house material, lighting, and angle
    2. The Integration (Action): Uses strong connection verbs for proper physical connections
    3. The Style Enforcers: Keywords for realism and quality
    4. The Negative Prompt: Hardcoded to prevent physics hallucinations
    
    Args:
        identified_problem: The identified accessibility barrier/problem (e.g., from barrier_detected)
        proposed_solution: The proposed renovation solution (e.g., from renovation_suggestion)
        mask_prompt: Description of the area to modify
        is_structural: Whether this is a structural renovation requiring removal
        clear_mask: For structural: description of object to be removed
        clear_prompt: For structural: what should replace the removed object
        build_mask: For structural: wider area description for construction
        build_prompt: For structural: detailed prompt for new accessible features
        wheelchair_accessible: If True, focus on wheelchair-accessible modifications
        
    Returns:
        A tuple of (main_prompt, negative_prompt) where:
        - main_prompt: The complete structured prompt combining all components
        - negative_prompt: The hardcoded negative prompt
    """
    # Use build_mask and build_prompt if provided (more specific), otherwise use mask_prompt and proposed_solution
    effective_mask = build_mask if (is_structural and build_mask) else mask_prompt
    effective_solution = build_prompt if (is_structural and build_prompt) else proposed_solution
    
    # Check if this is a case where no modification is needed
    problem_lower = identified_problem.lower()
    solution_lower = effective_solution.lower()
    if "no barriers" in problem_lower or "no accessibility barriers" in problem_lower or "already accessible" in problem_lower:
        # Return a prompt that explicitly says not to modify
        main_prompt = f"""This room has been assessed and NO accessibility barriers were detected. 
The room is already accessible and compliant. 
DO NOT modify this image in any way. 
Return the image exactly as it is, unchanged.
DO NOT create new walls, partitions, or any structural elements.
DO NOT add any new features.
Preserve the image exactly as provided."""
        return main_prompt, NEGATIVE_PROMPT
    
    # Component 1: The Anchor (Context)
    anchor = _extract_anchor_context(identified_problem, effective_solution, effective_mask)
    
    # Component 2: The Integration (Action)
    integration = _construct_integration_action(identified_problem, effective_solution, effective_mask)
    
    # Component 3: The Style Enforcers (already defined as constant)
    style_enforcers = STYLE_ENFORCERS
    
    # For structural renovations, add removal context
    removal_context = ""
    if is_structural and clear_mask and clear_prompt:
        removal_context = f"First, remove {clear_mask} and replace with {clear_prompt}, seamlessly blending with surrounding materials. Then, "
    
    # Construct the main prompt
    main_prompt = f"""You are an expert architectural in-painting specialist performing a precise accessibility renovation.

CRITICAL: ROOM ASSESSMENT FIRST
Before making any changes, assess if this room actually needs modification:
- If the room is already accessible and has no barriers, DO NOT modify anything - return the image unchanged
- Only modify rooms that have identified accessibility barriers
- If the barrier has already been addressed or doesn't exist, DO NOT create new modifications
- DO NOT modify rooms that are already compliant with accessibility standards

ANCHOR (CONTEXT):
The existing structure features: {anchor}. Analyze the current materials, lighting conditions, and viewing perspective to ensure perfect integration. Match the existing material textures, colors, and finishes exactly.

INTEGRATION (ACTION):
{removal_context}{integration}. Ensure all connections are physically sound and visible:
- Ramps must connect to BOTH surfaces with proper foundation - bottom edge flush against lower surface, top edge flush against upper surface
- Grab bars must be wall-mounted with visible anchors - flush against wall surface, properly secured to wall studs
- Handrails must be attached to walls or posts with visible brackets - properly supported, allowing free passage
- All modifications must maintain structural integrity and show proper weight distribution
- NO floating structures - everything must have visible connection points and support

STYLE ENFORCERS:
{style_enforcers}. The renovation must appear as if it was part of the original construction, with matching materials, textures, colors, and finishes. All new elements must blend seamlessly with existing architecture.

NEGATIVE PROMPT (ABSOLUTELY FORBIDDEN - DO NOT CREATE):
DO NOT generate under ANY circumstances: {NEGATIVE_PROMPT}. 
CRITICAL PROHIBITIONS:
- NEVER create new walls, partitions, barriers, or structural divisions
- NEVER build new walls, construct new walls, or add new walls
- NEVER create new room divisions or partitions
- NEVER build new staircases or structural elements
- These elements are STRICTLY FORBIDDEN and will result in physically impossible or unsafe structures
- If you are unsure, DO NOT add anything - preserve the existing structure exactly as it is

SPATIAL CONSTRAINTS (CRITICAL):
- Analyze the exact location: {effective_mask if effective_mask else "the area described in the renovation solution"}
- Identify all adjacent elements: driveways, pathways, doors, walls, furniture - these MUST remain unobstructed
- Verify the solution fits within available space without blocking access points
- Ensure ramps have clear space extending 36 inches beyond ends and do NOT block driveways or pathways
- Verify handrails are OPEN (not fences or cages) - people must pass by freely on both sides
- Check that all connections are physically possible and properly supported
- ABSOLUTELY DO NOT create new walls, partitions, barriers, staircases, or any new structural elements
- ONLY modify existing elements or add simple safety features (grab bars, handrails) to existing walls
- NEVER create new architectural features that didn't exist before
- Verify all ramps connect properly - no gaps, no floating, no disconnected ends

AODA COMPLIANCE:
- Ramp slopes: maximum 1:12 ratio (1 inch rise per 12 inches of run)
- Handrail heights: 34-38 inches above walking surface
- Grab bar heights: 33-36 inches above floor
- Doorway clear width: minimum 32 inches (preferably 36 inches)
- All safety features must support 250+ lbs
- Ramps must have proper landing areas at top and bottom

GENERATION REQUIREMENTS:
- FIRST: Assess if modification is actually needed - if room is already accessible, return unchanged
- Preserve ALL surrounding context exactly - do not modify unrelated areas
- Only change the specified barrier region - nothing else
- DO NOT create new walls, partitions, or structural elements
- ONLY add simple safety features (grab bars, handrails) to existing walls or surfaces
- ONLY modify existing elements (widen doorways, replace floors, add ramps to existing transitions)
- Ensure all additions are properly connected and supported (no floating structures, no disconnected elements)
- Maintain realistic proportions, shadows, and perspective
- Match existing architectural style, materials, and lighting conditions
- Show proper weight distribution and structural support for all new elements
- Display visible connection points: wall anchors for grab bars, foundation for ramps, brackets for handrails
- Ensure all surfaces connect properly: ramps must touch both surfaces, grab bars must touch walls, handrails must touch supports
- If uncertain about whether to modify, DO NOT modify - preserve the original"""
    
    # Component 4: The Negative Prompt (hardcoded)
    negative_prompt = NEGATIVE_PROMPT
    
    return main_prompt, negative_prompt


def get_structural_renovation_prompt(clear_mask: str, clear_prompt: str, build_mask: str, build_prompt: str, wheelchair_accessible: bool = False) -> str:
    """
    Returns the reasoning prompt for structural renovations requiring removal.
    Uses the new Structured Architectural In-painting format.
    
    Args:
        clear_mask: Description of object to be removed
        clear_prompt: What should replace the removed object
        build_mask: Wider area description for construction
        build_prompt: Detailed prompt for new accessible features
        wheelchair_accessible: If True, focus on wheelchair-accessible modifications
        
    Returns:
        The formatted reasoning prompt for structural renovations
    """
    # Extract problem and solution from the prompts
    identified_problem = clear_mask  # The barrier being removed
    proposed_solution = build_prompt  # The new accessible feature
    
    main_prompt, _ = generate_structured_architectural_prompt(
        identified_problem=identified_problem,
        proposed_solution=proposed_solution,
        mask_prompt=build_mask,
        is_structural=True,
        clear_mask=clear_mask,
        clear_prompt=clear_prompt,
        build_mask=build_mask,
        build_prompt=build_prompt,
        wheelchair_accessible=wheelchair_accessible
    )
    
    return main_prompt


def get_non_structural_renovation_prompt(mask_prompt: str, prompt: str, wheelchair_accessible: bool = False) -> str:
    """
    Returns the reasoning prompt for non-structural renovations (direct modifications).
    Uses the new Structured Architectural In-painting format.
    
    Args:
        mask_prompt: Description of the area to modify
        prompt: The renovation prompt describing what to add/change
        wheelchair_accessible: If True, focus on wheelchair-accessible modifications
        
    Returns:
        The formatted reasoning prompt for non-structural renovations
    """
    # Extract problem and solution from the prompts
    # For non-structural, we infer the problem from the area description
    identified_problem = mask_prompt  # The area needing modification
    proposed_solution = prompt  # The accessibility improvement
    
    main_prompt, _ = generate_structured_architectural_prompt(
        identified_problem=identified_problem,
        proposed_solution=proposed_solution,
        mask_prompt=mask_prompt,
        is_structural=False,
        wheelchair_accessible=wheelchair_accessible
    )
    
    return main_prompt

